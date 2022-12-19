import 'package:flutter/material.dart';
import 'package:frontend/data/model/product.dart';

class PopularItem extends StatelessWidget {
  const PopularItem({Key? key, required this.data, this.onTap})
      : super(key: key);
  final Product data;
  final GestureTapCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.only(right: 15),
        height: 170, width: 220,
        // color: secondary,
        child: Stack(
          children: [
            Positioned(
              top: 10,
              child: Container(
                height: 120,
                width: 220,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(15),
                  image: DecorationImage(
                      fit: BoxFit.cover, image: NetworkImage(data.image)),
                ),
              ),
            ),
            Positioned(
              top: 140,
              child: SizedBox(
                  width: 220,
                  child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Expanded(
                              child: Text(
                                data.name,
                                style: const TextStyle(
                                    fontSize: 14, fontWeight: FontWeight.w600),
                              ),
                            ),
                            const SizedBox(width: 5),
                            Text(
                              data.price.toString(),
                              style: const TextStyle(
                                  fontSize: 14,
                                  color: Colors.white,
                                  fontWeight: FontWeight.w600),
                            ),
                          ],
                        ),
                      ])),
            )
          ],
        ),
      ),
    );
  }
}
