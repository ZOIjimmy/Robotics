import 'dart:convert';

import 'package:frontend/data/model/product.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LocalDataStore {
  static const _keyOrders = "KEY_ORDERS";

  final SharedPreferences _prefs;

  LocalDataStore({required SharedPreferences prefs}) : _prefs = prefs;

  Future<void> setOrders(Product product, int size, int sugar, int milk) async {
    List<String>? currentOrders = _prefs.getStringList(_keyOrders);
    Object data = {
      'product': product.toJson(),
      'size': size.toString(),
      'sugar': sugar.toString(),
      'milk': milk.toString()
    };
    String string = jsonEncode(data);
    if (currentOrders == null) {
      await _prefs.setStringList(_keyOrders, [string]);
    } else {
      await _prefs.setStringList(_keyOrders, [...currentOrders, string]);
    }
  }

  List<Map> getOrders() {
    List<String> productAndOpt = _prefs.getStringList(_keyOrders) ?? [];
    print(productAndOpt);
    return List.from(productAndOpt.map((e) {
      Map<String, dynamic> data = json.decode(e);
      return Map.from({
        'product': Product.fromJson(data['product']!),
        'size': data['size'],
        'sugar': data['sugar'],
        'milk': data['milk']
      });
    }));
  }
}
