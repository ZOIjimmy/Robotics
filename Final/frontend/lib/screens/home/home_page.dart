import 'package:curved_navigation_bar/curved_navigation_bar.dart';
import 'package:flutter/material.dart';
import 'package:frontend/screens/home/home_tabs.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final _selectedTab = ValueNotifier(HomeTabs.order);

  List<IconData> tapIcons = [
    Icons.home_rounded,
    Icons.explore_rounded,
    Icons.shopping_cart_rounded,
    Icons.person_rounded
  ];

  @override
  Widget build(BuildContext context) {
    return _buildScaffold();
  }

  Widget _buildScaffold() {
    return ValueListenableBuilder<HomeTabs>(
      valueListenable: _selectedTab,
      builder: (context, tab, _) {
        return Scaffold(
          backgroundColor: tab.getColor(),
          extendBody: true,
          bottomNavigationBar: _buildBottomNavBar(),
          body: SafeArea(
            child: Column(
              children: [Expanded(child: tab.getPage())],
            ),
          ),
        );
      },
    );
  }

  Widget _buildBottomNavBar() {
    return CurvedNavigationBar(
      backgroundColor: Colors.transparent,
      items: const <Widget>[
        Icon(Icons.add, size: 30),
        Icon(Icons.list, size: 30),
        Icon(Icons.compare_arrows, size: 30),
      ],
      onTap: (index) {
        //Handle button tap
        _selectedTab.value = HomeTabs.values[index];
      },
    );
  }
}
