import os
import json
import google.generativeai as genai
from database import get_user_spending_analysis, get_all_credit_cards, get_user_by_id

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)

def calculate_card_value(card: dict, spending: dict):
    annual_income = spending["estimated_annual_income"]
    credit_score = spending["estimated_credit_score"]
    
    min_income = card.get("minimum_income", 0) or 0
    min_score = card.get("minimum_credit_score", 600) or 600
    
    is_eligible = (annual_income >= min_income) and (credit_score >= min_score)
    if not is_eligible:
        return None
        
    cat_breakdown = spending["category_breakdown"]
    total_annual_spend = spending["annualized_spending"]
    
    gross_rewards = 0.0
    category_contributions = {}
    
    cat_map = {
        "Travel": "travel_reward",
        "Flights": "travel_reward",
        "Hotels": "travel_reward",
        "Shopping": "shopping_reward",
        "Apparel": "shopping_reward",
        "Electronics": "shopping_reward",
        "Online Shopping": "online_reward",
        "Food": "food_reward",
        "Restaurants": "food_reward",
        "Dining": "food_reward",
        "Groceries": "grocery_reward",
        "Supermarket": "grocery_reward",
        "Fuel": "fuel_reward",
        "Utilities": "utility_reward",
        "Electricity": "utility_reward",
        "Telecom": "utility_reward",
        "Mobile Recharge": "utility_reward",
        "Entertainment": "online_reward",
        "Movies": "online_reward",
        "Transport": "offline_reward",
        "Cab": "online_reward"
    }
    
    base_rate = card.get("reward_rate", 1.0) or 1.0
    
    for cat, amount in cat_breakdown.items():
        reward_field = cat_map.get(cat, "reward_rate")
        rate = card.get(reward_field, 0.0) or 0.0
        if rate <= 0:
            rate = base_rate
            
        reward_amt = (amount * rate) / 100.0
        gross_rewards += reward_amt
        category_contributions[cat] = round(reward_amt, 2)
        
    reward_cap = card.get("reward_cap", 0) or 0
    if reward_cap > 0 and gross_rewards > reward_cap * 12:
        gross_rewards = reward_cap * 12
        
    annual_fee = card.get("annual_fee", 0.0) or 0.0
    waiver_spend = card.get("annual_fee_waiver_spend", 0.0) or 0.0
    
    if waiver_spend > 0 and total_annual_spend >= waiver_spend:
        effective_annual_fee = 0.0
    else:
        effective_annual_fee = annual_fee
        
    net_annual_value = gross_rewards - effective_annual_fee
    
    return {
        "card_id": card["card_id"],
        "card_name": card["card_name"],
        "bank_name": card["bank_name"],
        "card_network": card["card_network"],
        "card_type": card["card_type"],
        "image_path": card["image_path"],
        "apply_url": card.get("apply_url", "https://www.google.com/search?q=" + card["card_name"]),
        "annual_fee": annual_fee,
        "effective_annual_fee": effective_annual_fee,
        "reward_type": card["reward_type"],
        "minimum_income": min_income,
        "gross_rewards": round(gross_rewards, 2),
        "net_annual_value": round(net_annual_value, 2),
        "category_contributions": category_contributions,
        "raw_card": card
    }

def get_recommendations_for_user(user_id: str, category_filter: str = "All"):
    user = get_user_by_id(user_id)
    if not user:
        return None
        
    spending = get_user_spending_analysis(user_id)
    all_cards = get_all_credit_cards()
    
    eligible_evaluated = []
    for c in all_cards:
        val = calculate_card_value(c, spending)
        if val is not None:
            eligible_evaluated.append(val)
            
    # Dynamic Category Filtering & Category-Specific Ranking (Requirement 6)
    if category_filter and category_filter != "All":
        cat_lower = category_filter.lower()
        filtered = []
        for item in eligible_evaluated:
            card = item["raw_card"]
            if cat_lower == "shopping":
                score = max(card.get("shopping_reward", 0), card.get("online_reward", 0))
                if score > 0 or "shopping" in card.get("card_type", "").lower() or "cashback" in card.get("card_type", "").lower():
                    item["cat_score"] = score
                    filtered.append(item)
            elif cat_lower == "travel":
                score = card.get("travel_reward", 0)
                if score > 0 or "travel" in card.get("card_name", "").lower() or "vistara" in card.get("card_name", "").lower() or "miles" in card.get("reward_type", "").lower():
                    item["cat_score"] = score
                    filtered.append(item)
            elif cat_lower == "utilities":
                score = card.get("utility_reward", 0)
                if score > 0 or "utility" in card.get("card_type", "").lower() or "bill" in card.get("card_name", "").lower() or "ace" in card.get("card_id", "").lower():
                    item["cat_score"] = score
                    filtered.append(item)
            elif cat_lower == "food":
                score = max(card.get("food_reward", 0), card.get("grocery_reward", 0))
                if score > 0 or "food" in card.get("card_type", "").lower() or "zomato" in card.get("card_name", "").lower() or "swiggy" in card.get("eligibility_notes", "").lower() or "eazydiner" in card.get("card_name", "").lower():
                    item["cat_score"] = score
                    filtered.append(item)
                    
        if filtered:
            # Sort by category-specific score then net annual value
            filtered.sort(key=lambda x: (x.get("cat_score", 0), x["net_annual_value"]), reverse=True)
            eligible_evaluated = filtered

    if category_filter == "All":
        eligible_evaluated.sort(key=lambda x: x["net_annual_value"], reverse=True)
        
    top_candidates = eligible_evaluated[:8]
    ai_recommendations = call_gemini_recommendation_engine(user, spending, top_candidates, category_filter)
    
    if not ai_recommendations:
        ai_recommendations = fallback_recommendations(top_candidates, spending, category_filter)
        
    return {
        "user": user,
        "spending_summary": spending,
        "recommendations": ai_recommendations[:5]
    }

def call_gemini_recommendation_engine(user: dict, spending: dict, candidates: list, category_filter: str = "All"):
    if not candidates:
        return []
        
    try:
        model = genai.GenerativeModel("gemini-3.8-flash")
        
        prompt = f"""
You are the AI credit card recommendation engine for "Credit-It".
Analyze user {user['name']} with annual spend ₹{spending['annualized_spending']:,.0f} under category filter "{category_filter}".

CANDIDATE CARDS:
{json.dumps([{
    'card_id': c['card_id'],
    'card_name': c['card_name'],
    'net_annual_value': c['net_annual_value'],
    'annual_fee': c['annual_fee'],
    'reward_type': c['reward_type'],
    'category_contributions': c['category_contributions']
} for c in candidates], indent=2)}

Rank top cards for "{category_filter}" category spend and return JSON:
{{
  "ai_insight_summary": "Calculated based on your annual spending profile across different merchant categories.",
  "ranked_cards": [
    {{
      "card_id": "card_id_here",
      "ai_summary": "Short 1 sentence summary focusing on {category_filter} rewards...",
      "personalized_explanation": "Detailed multi-paragraph explanation...",
      "top_contributing_categories": ["Category 1", "Category 2"]
    }}
  ]
}}
"""
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
            
        data = json.loads(text)
        cand_map = {c["card_id"]: c for c in candidates}
        result = []
        for r in data.get("ranked_cards", []):
            cid = r["card_id"]
            if cid in cand_map:
                c_data = cand_map[cid]
                merged = {**c_data}
                merged["ai_summary"] = r.get("ai_summary", f"Delivers +₹{c_data['net_annual_value']:,.0f}/yr in net value.")
                merged["personalized_explanation"] = r.get("personalized_explanation", "")
                merged["top_contributing_categories"] = r.get("top_contributing_categories", list(c_data["category_contributions"].keys())[:3])
                result.append(merged)
                
        for c in candidates:
            if len(result) >= 5:
                break
            if c["card_id"] not in [x["card_id"] for x in result]:
                c_copy = {**c}
                c_copy["ai_summary"] = f"Delivers estimated +₹{c['net_annual_value']:,.0f}/yr net value based on your profile."
                c_copy["personalized_explanation"] = f"Recommended for {user['name']} based on your annual spend of ₹{spending['annualized_spending']:,.0f}."
                c_copy["top_contributing_categories"] = list(c["category_contributions"].keys())[:3]
                result.append(c_copy)
                
        return result
        
    except Exception as e:
        print(f"Gemini API rate limit or network exception: {e}. Executing rule-based recommendation fallback.")
        return fallback_recommendations(candidates, spending, category_filter)

def fallback_recommendations(candidates: list, spending: dict, category_filter: str = "All"):
    result = []
    for c in candidates[:5]:
        top_cats = sorted(c["category_contributions"].items(), key=lambda x: x[1], reverse=True)[:3]
        top_cat_names = [k for k, v in top_cats]
        top_cat_str = ", ".join(top_cat_names) if top_cat_names else "general spends"
        
        filter_tag = f" for {category_filter}" if category_filter != "All" else ""
        ai_sum = f"Top recommendation{filter_tag}: Delivers +₹{c['net_annual_value']:,.0f}/yr net annual value with strong returns on {top_cat_str}."
        
        explanation = f"""Based on your historical transaction analysis, your annual spending of ₹{spending['annualized_spending']:,.0f} aligns exceptionally well with the reward structure of {c['card_name']}.

The primary driver for this recommendation is your strong spending in {top_cat_str}. With an annual fee of ₹{c['annual_fee']:,.0f} (which may be waived on meeting spend milestones), the expected gross annual rewards of ₹{c['gross_rewards']:,.0f} provide a net annual value of ₹{c['net_annual_value']:,.0f}.

Furthermore, the card's complimentary perks including lounge access and category rewards make it a top financial fit for your profile."""

        c_copy = {**c}
        c_copy["ai_summary"] = ai_sum
        c_copy["personalized_explanation"] = explanation
        c_copy["top_contributing_categories"] = top_cat_names
        result.append(c_copy)
    return result
