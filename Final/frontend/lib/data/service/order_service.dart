import 'package:dio/dio.dart';
import 'package:frontend/data/model/product.dart';
import 'package:frontend/data/service/local_data.dart';
import 'package:get_it/get_it.dart';

class OrderService {
  final String _baseUrl;

  OrderService({required String url}) : _baseUrl = url;

  Future order(int size, int sugar, int milk, Product product) async {
    String urlPart = "";
    Map<String, String> body = {
      "size": size.toString(),
      "sugar": sugar.toString(),
      "milk": milk.toString()
    };

    final url = Uri.parse('$_baseUrl$urlPart').toString();
    final dio = Dio();
    final response = await dio.post(url, data: body);
    if (response.statusCode == 201) {
      final LocalDataStore localDataStore =
          GetIt.instance.get<LocalDataStore>();
      await localDataStore.setOrders(product, size, sugar, milk);
      // final res = LoginResponse.fromJson(response.body);
      print(response);
      return response;
    }
  }
}
