import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:frontend/components/feature.dart';
import 'package:frontend/components/popular.dart';
import 'package:frontend/components/text_box.dart';
import 'package:frontend/data/model/product.dart';
import 'package:frontend/screens/home/components/notification.dart';
import 'package:frontend/screens/home/item/item_detail.dart';

import 'package:http/http.dart' as http;

class MenuPage extends StatelessWidget {
  MenuPage({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
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
                    ))),
            const NotificationBox(
              number: 1,
            )
          ],
        ),
      ),
      body: buildMain(context),
    );
  }

  Widget buildMain(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const SizedBox(
            height: 10,
          ),
          Container(
            margin: const EdgeInsets.only(left: 15, right: 15),
            child: const Text(
              "Find Your Meals",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
          ),
          const SizedBox(
            height: 20,
          ),
          Container(
              margin: EdgeInsets.only(left: 15, right: 15),
              child: CustomTextBox(
                  hint: "Search",
                  prefix: Icon(Icons.search, color: Colors.black),
                  suffix:
                      Icon(Icons.filter_list_outlined, color: Colors.black))),
          const SizedBox(
            height: 25,
          ),
          Container(
            margin: EdgeInsets.only(left: 15, right: 15),
            height: 150,
            decoration: BoxDecoration(
                color: Colors.grey,
                borderRadius: BorderRadius.circular(15),
                image: DecorationImage(
                    fit: BoxFit.cover,
                    image: NetworkImage(
                      "https://images.unsplash.com/photo-1504674900247-0877df9cc836?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTF8fHByb2ZpbGV8ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
                    ))),
          ),
          SizedBox(
            height: 20,
          ),
          Container(
            margin: EdgeInsets.only(left: 15, right: 15),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  "Recent",
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                Text(
                  "See all",
                  style: TextStyle(fontSize: 14),
                ),
              ],
            ),
          ),
          SizedBox(
            height: 5,
          ),
          Container(
            child: listPopulars(),
          ),
          SizedBox(
            height: 20,
          ),
          Container(
            margin: EdgeInsets.only(left: 15, right: 15),
            child: Text(
              "Featured",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
          ),
          SizedBox(
            height: 10,
          ),
          Container(
            margin: EdgeInsets.only(left: 15, right: 15),
            child: listFeatured(context),
          ),
          SizedBox(
            height: 20,
          ),
        ],
      ),
    );
  }

  final recent = [
    {"name": "test", "image": "test", "price": "price"},
    {"name": "test", "image": "test", "price": "price"}
  ];

  listPopulars() {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      padding: const EdgeInsets.only(left: 15),
      child: Row(
        children: List.generate(
            recent.length, (index) => PopularItem(data: recent[index])),
      ),
    );
  }

  final featured = [
    {
      "name": "test",
      "image": "test",
      "sources": "",
      "rate": "",
      "rate_number": "",
      "price": "price"
    },
    {
      "name": "test",
      "image": "test",
      "sources": "",
      "rate": "",
      "rate_number": "",
      "price": "price"
    }
  ];

  final List<Product> productList = [
    Product(
        name: "name",
        price: 300,
        about: "about",
        isAvailable: true,
        off: 0,
        quantity: 10,
        images: [""],
        isLiked: false,
        rating: 3.0,
        type: ProductType.mobile),
  ];

  listFeatured(BuildContext context) {
    return Column(
      children: List.generate(
          featured.length,
          (index) => FeaturedItem(
                data: featured[index],
                onTap: () async {
                  print("send http");
                  final url = Uri.parse('http://linux9.csie.ntu.edu.tw:13751');
                  try {
                    final response = await http.get(url);
                    print(response);
                    print(response.body);
                  } catch (e) {
                    print(e.runtimeType);
                  }
                  // Navigator.of(context).push(
                  //   MaterialPageRoute(
                  //     builder: (context) => ItemPage(productList[0]),
                  //   ),
                  // );
                },
              )),
    );
  }
}
