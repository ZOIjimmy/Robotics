import 'package:flutter/material.dart';
import 'package:frontend/screens/home/cart/cart_page.dart';
import 'package:frontend/screens/home/menu/menu_page.dart';

enum HomeTabs {
  menuList,
  order,
}

extension MainTabsExt on HomeTabs {
  String getLabel() {
    switch (this) {
      case HomeTabs.menuList:
        return "菜單";
      case HomeTabs.order:
        return "已點項目";
    }
  }

  Widget getPage() {
    switch (this) {
      case HomeTabs.menuList:
        return MenuPage();
      case HomeTabs.order:
        return CartPage();
    }
  }

  MaterialColor getColor() {
    switch (this) {
      case HomeTabs.menuList:
        return Colors.amber;
      case HomeTabs.order:
        return Colors.cyan;
    }
  }
}
