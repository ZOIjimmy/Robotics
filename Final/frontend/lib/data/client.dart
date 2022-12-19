import 'package:frontend/data/service/local_data.dart';
import 'package:frontend/data/service/menu_service.dart';
import 'package:frontend/data/service/order_service.dart';
import 'package:frontend/environments/environment_singleton.dart';
import 'package:get_it/get_it.dart';
import 'package:shared_preferences/shared_preferences.dart';

initClientDI(GetIt getIt) async {
  String url = Environment().config.baseUrl;
  print('Base Url: $url');
  getIt.registerLazySingleton(() => MenuService(url: url));

  getIt.registerLazySingleton(() => OrderService(url: url));

  final sharedPrefs = await SharedPreferences.getInstance();
  getIt.registerLazySingleton(() => LocalDataStore(prefs: sharedPrefs));
}
