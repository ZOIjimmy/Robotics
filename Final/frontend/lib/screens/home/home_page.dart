import 'package:curved_navigation_bar/curved_navigation_bar.dart';
import 'package:flutter/material.dart';
import 'package:frontend/screens/home/home_tabs.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final _selectedTab = ValueNotifier(HomeTabs.menuList);

  @override
  Widget build(BuildContext context) {
    return buildScaffold();
  }

  Widget buildScaffold() {
    return ValueListenableBuilder<HomeTabs>(
      valueListenable: _selectedTab,
      builder: (context, tab, _) {
        return Scaffold(
          backgroundColor: tab.getColor(),
          extendBody: true,
          bottomNavigationBar: buildBottomNavBar(),
          body: SafeArea(
            child: Column(
              children: [
                Expanded(child: tab.getPage()),
                const SizedBox(height: 30)
              ],
            ),
          ),
        );
      },
    );
  }

  Widget buildBottomNavBar() {
    return CurvedNavigationBar(
      backgroundColor: Colors.transparent,
      items: const <Widget>[
        Icon(Icons.add, size: 30),
        Icon(Icons.list, size: 30),
      ],
      onTap: (index) {
        _selectedTab.value = HomeTabs.values[index];
      },
    );
  }
}
