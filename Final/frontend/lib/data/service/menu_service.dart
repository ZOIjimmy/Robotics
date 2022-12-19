import 'package:dio/dio.dart';
import 'package:http/http.dart' as http;

class MenuService {
  final String _baseUrl;

  MenuService({required String url}) : _baseUrl = url;

  Future test_get(String urlPart) async {
    var dio = Dio();
    final url = Uri.parse('$_baseUrl$urlPart');
    final response = await http.get(url);
    print(response);
    if (response.statusCode == 200) {
      // final res = LoginResponse.fromJson(response.body);
      print(response);
      return response;
    } else {
      final body = response.body;
      if (body.contains("UserDisabled")) {
        throw Exception();
      } else {
        throw Exception();
      }
    }
  }

  Future test_post(String urlPart, Map<String, String> body) async {
    final url = Uri.parse('$_baseUrl$urlPart');
    final response = await http.post(url, body: body);
    if (response.statusCode == 201) {
      // final res = LoginResponse.fromJson(response.body);
      print(response);
      return response;
    } else {
      final body = response.body;
      if (body.contains("UserDisabled")) {
        throw Exception();
      } else {
        throw Exception();
      }
    }
  }
}
