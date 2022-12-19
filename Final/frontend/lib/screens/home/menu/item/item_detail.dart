import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:frontend/data/model/product.dart';
import 'package:frontend/data/service/order_service.dart';
import 'package:get_it/get_it.dart';
import 'package:syncfusion_flutter_sliders/sliders.dart';

class ItemPage extends StatefulWidget {
  const ItemPage(this.product, {Key? key}) : super(key: key);

  final Product product;

  @override
  State<ItemPage> createState() => _ItemPageState();
}

class _ItemPageState extends State<ItemPage> {
  double _sizeSliderValue = 20;
  double _sugarSliderValue = 20;
  double _milkSliderValue = 20;

  @override
  Widget build(BuildContext context) {
    double height = MediaQuery.of(context).size.height;
    double width = MediaQuery.of(context).size.width;

    return SafeArea(
      child: Scaffold(
        extendBodyBehindAppBar: true,
        appBar: buildAppBar(context),
        body: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              buildProductImage(width, height),
              const SizedBox(height: 20),
              Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    buildName(context),
                    const SizedBox(height: 10),
                    buildPrice(context),
                    const SizedBox(height: 30),
                    buildDescription(context),
                    const SizedBox(height: 20),
                    buildCustomizeSliders(),
                    const SizedBox(height: 20),
                    buildButtonAdd(context)
                  ],
                ),
              )
            ],
          ),
        ),
      ),
    );
  }

  Widget buildSlider(String title, Color color, double valueState,
      void Function(dynamic)? onChange) {
    return Padding(
      padding: const EdgeInsets.all(30.0),
      child: Container(
        width: 150,
        decoration: BoxDecoration(
          color: color,
          borderRadius: const BorderRadius.all(
            Radius.circular(30),
          ),
        ),
        child: Column(children: [
          Text(title),
          SfSlider.vertical(
            min: 0.0,
            max: 100.0,
            value: valueState,
            interval: 20,
            showTicks: true,
            showLabels: true,
            enableTooltip: true,
            minorTicksPerInterval: 1,
            onChanged: onChange,
          )
        ]),
      ),
    );
  }

  Widget buildCustomizeSliders() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        buildSlider("水量", const Color(0xFFEB455F), _sizeSliderValue,
            (dynamic value) {
          setState(() {
            _sizeSliderValue = value;
          });
        }),
        const SizedBox(width: 20),
        buildSlider("糖量", const Color(0xFFFCFFE7), _sugarSliderValue,
            (dynamic value) {
          setState(() {
            _sugarSliderValue = value;
          });
        }),
        const SizedBox(width: 20),
        buildSlider("牛奶量", const Color(0xFFBAD7E9), _milkSliderValue,
            (dynamic value) {
          setState(() {
            _milkSliderValue = value;
          });
        }),
      ],
    );
  }

  PreferredSizeWidget buildAppBar(BuildContext context) {
    return AppBar(
      backgroundColor: Colors.transparent,
      elevation: 0,
      leading: IconButton(
        onPressed: () {
          Navigator.pop(context);
        },
        icon: const Icon(
          Icons.arrow_back,
          color: Colors.black,
        ),
      ),
    );
  }

  Widget buildProductImage(double width, double height) {
    final product = widget.product;

    return SizedBox(
      height: height * 0.32,
      width: width,
      child: CachedNetworkImage(fit: BoxFit.cover, imageUrl: product.image),
    );
  }

  Text buildName(BuildContext context) {
    return Text(
      widget.product.name,
      style: Theme.of(context).textTheme.headline2,
    );
  }

  Row buildPrice(BuildContext context) {
    final product = widget.product;

    return Row(
      children: [
        Text(
          product.off != null ? "\$${product.off}" : "\$${product.price}",
          style: const TextStyle(
            decoration: TextDecoration.lineThrough,
            color: Colors.grey,
            fontWeight: FontWeight.w200,
            fontSize: 30,
          ),
        ),
        const SizedBox(width: 3),
        Visibility(
          visible: product.off != null ? true : false,
          child: Text(
            "\$${product.price}",
            style: const TextStyle(
              color: Colors.grey,
              fontWeight: FontWeight.w200,
              fontSize: 30,
            ),
          ),
        ),
        const Spacer(),
        Text(
          product.isAvailable ? "尚有庫存" : "抱歉補貨中",
          style: const TextStyle(fontWeight: FontWeight.w500),
        )
      ],
    );
  }

  Widget buildDescription(BuildContext context) {
    return Container(
      alignment: Alignment.center,
      decoration: const BoxDecoration(
        color: Color(0xFFE5E6E8),
        borderRadius: BorderRadius.all(
          Radius.circular(100),
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.all(30.0),
        child: Column(children: [
          Text(
            "茶葉故事",
            style: Theme.of(context).textTheme.headline4,
          ),
          const SizedBox(height: 10),
          Text(widget.product.about)
        ]),
      ),
    );
  }

  SizedBox buildButtonAdd(BuildContext context) {
    final OrderService orderService = GetIt.instance.get<OrderService>();

    return SizedBox(
      width: double.infinity,
      child: ElevatedButton(
        onPressed: widget.product.isAvailable
            ? () {
                orderService.order(
                    _sizeSliderValue.round(),
                    _sugarSliderValue.round(),
                    _milkSliderValue.round(),
                    widget.product);
                Navigator.of(context).pop();
              }
            : null,
        child: const Text("點餐"),
      ),
    );
  }
}


// Slider(
//   value: _sizeSliderValue,
//   max: 100,
//   divisions: 100,
//   label: _sizeSliderValue.round().toString(),
//   onChanged: (double value) {
//     setState(() {
//       _sizeSliderValue = value;
//     });
//   },
// ),