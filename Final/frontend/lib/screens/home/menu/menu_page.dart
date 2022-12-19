import 'package:flutter/material.dart';
import 'package:frontend/components/feature.dart';
import 'package:frontend/components/popular.dart';
import 'package:frontend/components/text_box.dart';
import 'package:frontend/data/model/product.dart';
import 'package:frontend/data/service/local_data.dart';
import 'package:frontend/data/service/menu_service.dart';
import 'package:frontend/screens/home/components/notification.dart';
import 'package:frontend/screens/home/menu/item/item_detail.dart';
import 'package:get_it/get_it.dart';

class MenuPage extends StatelessWidget {
  MenuPage({Key? key}) : super(key: key);

  final MenuService _menuService = GetIt.instance.get<MenuService>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,
      appBar: buildAppBar(),
      body: buildMain(context),
    );
  }

  AppBar buildAppBar() {
    return AppBar(
      backgroundColor: Colors.transparent,
      automaticallyImplyLeading: false,
      elevation: 0,
      title: Row(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Expanded(
            child: Container(
              alignment: Alignment.centerLeft,
              child: const Icon(
                Icons.clear_all_rounded,
                size: 28,
              ),
            ),
          ),
          const NotificationBox(
            number: 0,
          )
        ],
      ),
    );
  }

  Widget buildMain(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const SizedBox(height: 10),
          buildTitle(),
          const SizedBox(height: 20),
          buildSearchBar(),
          const SizedBox(height: 25),
          buildImageBanner(),
          const SizedBox(height: 20),
          buildTitleRecent(),
          const SizedBox(height: 5),
          buildPopulars(),
          const SizedBox(height: 20),
          buildTextProducts(),
          const SizedBox(height: 10),
          buildProductList(context),
          const SizedBox(height: 20),
        ],
      ),
    );
  }

  Widget buildTitle() {
    return Container(
      margin: const EdgeInsets.only(left: 15, right: 15),
      child: const Text(
        "I would like some...",
        style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
      ),
    );
  }

  Widget buildSearchBar() {
    return Container(
      margin: const EdgeInsets.only(left: 15, right: 15),
      child: CustomTextBox(
        hint: "Search",
        prefix: const Icon(Icons.search, color: Colors.black),
        suffix: const Icon(Icons.filter_list_outlined, color: Colors.black),
      ),
    );
  }

  Widget buildImageBanner() {
    return Container(
      margin: const EdgeInsets.only(left: 15, right: 15),
      height: 150,
      decoration: BoxDecoration(
          color: Colors.grey,
          borderRadius: BorderRadius.circular(15),
          image: const DecorationImage(
              fit: BoxFit.cover,
              image: NetworkImage(
                  "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqwHY2u7Ys1eCHiIZQBciyV-xlRM70T_r06Q&usqp=CAU"))),
    );
  }

  Widget buildTitleRecent() {
    return Container(
      margin: EdgeInsets.only(left: 15, right: 15),
      child: const Text(
        "Recent",
        style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
      ),
    );
  }

  Widget buildPopulars() {
    final LocalDataStore _localdata = GetIt.instance.get<LocalDataStore>();

    final List<Product> recent = [productList[0]];

    return SizedBox(
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.only(left: 15),
        child: Row(
          children: List.generate(
            recent.length,
            (index) => PopularItem(data: recent[index]),
          ),
        ),
      ),
    );
  }

  Widget buildTextProducts() {
    return Container(
      margin: const EdgeInsets.only(left: 15, right: 15),
      child: const Text(
        "Products",
        style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
      ),
    );
  }

  final List<Product> productList = [
    Product(
      name: "魚池有茶",
      image:
          "https://img.cashier.ecpay.com.tw/image/2021/01/19/5819_caee1046be98b4ff2293914ceee024b26e20a827.jpg",
      rateNumber: 10,
      sources: "日月潭必買人氣伴手禮紅韻紅茶",
      price: 300,
      about:
          "✔紅韻紅茶榮獲2019日月潭紅茶評鑑優質獎 , ✔日月潭必買人氣伴手禮紅韻紅茶 , ✔茶湯水色金紅明亮光澤，香氣花果蜜香 , ✔三角立體茶包更能快速地釋放茶香, ✔精緻茶包罐裝",
      isAvailable: true,
      off: 0,
      quantity: 5,
    ),
    Product(
      name: "有記名茶",
      image:
          "https://images.squarespace-cdn.com/content/v1/57fdfbbf20099e2082ed0b04/1476686457817-W90UMOLAQHWINKZUW5QC/高山烏龍茶.JPG?format=1000w",
      rateNumber: 10,
      sources: "台北大稻埕 時尚人文，百年茶韻",
      price: 300,
      about: """
              【 台北大稻埕—台灣茶揚名世界的起點 】

                  時尚人文，百年茶韻。
                  依偎在淡水河邊，創立於1890年，
                  有記名茶早從南糖北茶的年代，就扮演著台灣茶外銷的重要推手；
                  誠信為本，傳承五代，百年茶廠，始終堅持在大稻埕，娓娓細訴著台灣茶美麗動人的故事！
            """,
      isAvailable: true,
      off: 0,
      quantity: 5,
    ),
    Product(
      name: "twinings",
      image:
          "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1t248ngoGn6g2UxLz3_w3j1kCl_9SElWnPQ&usqp=CAU",
      rateNumber: 10,
      sources: "經典調和風味，口感較為紮實飽滿，味道稍強勁",
      price: 300,
      about: """
                English Breakfast Tea 英倫早餐茶

                  經典調和風味，口感較為紮實飽滿，味道稍強勁，
                  混合阿薩姆及肯亞等味道鮮明的茶，帶有阿薩姆紅茶的特殊麥香。
                  適合搭配口味濃郁的英國傳統早餐，有助於去油解膩。
                  濃郁的口感亦適合用於調配英式奶茶。
            """,
      isAvailable: true,
      off: 0,
      quantity: 5,
    ),
  ];

  buildProductList(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(left: 15, right: 15),
      child: Column(
        children: List.generate(
          productList.length,
          (index) => FeaturedItem(
            data: productList[index],
            onTap: () async {
              Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (context) => ItemPage(productList[index]),
                ),
              );
            },
          ),
        ),
      ),
    );
  }
}
