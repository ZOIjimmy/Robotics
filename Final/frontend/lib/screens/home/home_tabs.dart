import 'package:flutter/material.dart';
import 'package:frontend/screens/home/menu_page.dart';

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
        return const MenuPage();
      case HomeTabs.order:
        return const MenuPage();
    }
  }
}
