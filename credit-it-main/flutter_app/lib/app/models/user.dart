class User {
  final String userId;
  final String name;
  final String email;
  final String phone;
  final String pan;
  final String dob;

  User({
    required this.userId,
    required this.name,
    required this.email,
    required this.phone,
    required this.pan,
    required this.dob,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      userId: json['user_id'] ?? '',
      name: json['name'] ?? '',
      email: json['email'] ?? '',
      phone: json['phone'] ?? '',
      pan: json['pan'] ?? '',
      dob: json['dob'] ?? '',
    );
  }

  String get initials {
    final parts = name.trim().split(' ');
    if (parts.length >= 2) {
      return '${parts[0][0]}${parts[1][0]}'.toUpperCase();
    } else if (parts.isNotEmpty && parts[0].isNotEmpty) {
      return parts[0][0].toUpperCase();
    }
    return 'U';
  }
}
