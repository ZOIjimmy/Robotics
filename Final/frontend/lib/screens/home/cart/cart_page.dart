import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:frontend/data/model/product.dart';
import 'package:frontend/data/service/local_data.dart';
import 'package:frontend/screens/home/cart/empty_cart.dart';
import 'package:get_it/get_it.dart';

// final ProductController controller = Get.put(ProductController());

class CartPage extends StatefulWidget {
  const CartPage({Key? key}) : super(key: key);

  @override
  CartPageState createState() => CartPageState();
}

class CartPageState extends State<CartPage> {
// class CartPage extends StatelessWidget {
  // CartPage({Key? key}) : super(key: key);

  final LocalDataStore localDataStore = GetIt.instance.get<LocalDataStore>();
  List<Map> data = [];
  @override
  void initState() {
    data = localDataStore.getOrders();
  }

  @override
  Widget build(BuildContext context) {
    // final List<Map> data = localDataStore.getOrders();

    return Scaffold(
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            flex: 10,
            child: data.isEmpty ? const EmptyCart() : buildCartListView(data),
          ),
          // buildBottomBarTitle(),
        ],
      ),
      backgroundColor: Colors.transparent,
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          await localDataStore.clearOrder();
          setState(() {
            data = localDataStore.getOrders();
          });
        },
        backgroundColor: Colors.green,
        child: const Icon(Icons.delete),
      ),
    );
  }

  PreferredSizeWidget buildAppBar(BuildContext context) {
    return AppBar(
      title: const Text("My cart"),
    );
  }

  Widget buildCartListView(List<Map> productList) {
    return ListView.builder(
      shrinkWrap: true,
      padding: const EdgeInsets.all(20),
      itemCount: productList.length,
      itemBuilder: (_, index) {
        Product product = productList[index]['product'];
        int size = int.parse(productList[index]['size']);
        int sugar = int.parse(productList[index]['sugar']);
        int milk = int.parse(productList[index]['milk']);
        return Container(
          margin: const EdgeInsets.only(bottom: 20),
          padding: const EdgeInsets.all(15),
          height: 120,
          decoration: BoxDecoration(
              color: Colors.grey[200]?.withOpacity(0.6),
              borderRadius: BorderRadius.circular(10)),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Container(
                padding: const EdgeInsets.all(5),
                decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(10),
                    color: Colors.amber),
                child: ClipRRect(
                  borderRadius: const BorderRadius.all(Radius.circular(10)),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(10),
                    child: CachedNetworkImage(
                      imageUrl: product.image,
                      width: 70,
                      height: 120,
                      fit: BoxFit.contain,
                    ),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.only(left: 10),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    Text(
                      product.name,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(
                          fontWeight: FontWeight.w600, fontSize: 15),
                    ),
                    Text(
                      "水量：$size  糖量：$sugar  牛奶量：$milk",
                      style: TextStyle(
                          color: Colors.black.withOpacity(0.5),
                          fontWeight: FontWeight.w400),
                    ),
                  ],
                ),
              ),
              const Spacer(),
              Container(
                decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(10)),
                child: Row(
                  children: [
                    // IconButton(
                    //   splashRadius: 10.0,
                    //   onPressed: () => {}, //TODO:
                    //   icon: const Icon(
                    //     Icons.remove,
                    //     color: Color(0xFFEC6813),
                    //   ),
                    // ),
                    // IconButton(
                    //   splashRadius: 10.0,
                    //   onPressed: () => {}, // TODO:
                    //   icon: const Icon(
                    //     Icons.add,
                    //     color: Color(0xFFEC6813),
                    //   ),
                    // ),
                  ],
                ),
              )
            ],
          ),
        );
      },
    );
  }

  // Widget buildBottomBarTitle() {
  //   return Expanded(
  //     flex: 1,
  //     child: Container(
  //       padding: const EdgeInsets.symmetric(horizontal: 30),
  //       child: Row(
  //         mainAxisAlignment: MainAxisAlignment.spaceBetween,
  //         children: const [
  //           Text("Total",
  //               style: TextStyle(fontSize: 22, fontWeight: FontWeight.w400)),
  //         ],
  //       ),
  //     ),
  //   );
  // }
}
