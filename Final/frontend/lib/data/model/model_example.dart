// import 'dart:convert';

// import 'package:frontend/data/model/user/user.dart';

// class LoginResponse {
//   final String accessToken;
//   final User user;

//   LoginResponse({
//     required this.accessToken,
//     required this.user,
//   });

//   LoginResponse copyWith({
//     String? accessToken,
//     User? user,
//   }) {
//     return LoginResponse(
//       accessToken: accessToken ?? this.accessToken,
//       user: user ?? this.user,
//     );
//   }

//   Map<String, dynamic> toMap() {
//     return {
//       'accessToken': accessToken,
//       'user': user.toMap(),
//     };
//   }

//   factory LoginResponse.fromMap(Map<String, dynamic> map) {
//     return LoginResponse(
//       accessToken: map['accessToken'],
//       user: User.fromMap(map['user']),
//     );
//   }

//   String toJson() => json.encode(toMap());

//   factory LoginResponse.fromJson(String source) =>
//       LoginResponse.fromMap(json.decode(source));

//   @override
//   String toString() => 'LoginResponse(accessToken: $accessToken, user: $user)';

//   @override
//   bool operator ==(Object other) {
//     if (identical(this, other)) return true;

//     return other is LoginResponse &&
//         other.accessToken == accessToken &&
//         other.user == user;
//   }

//   @override
//   int get hashCode => accessToken.hashCode ^ user.hashCode;
// }
