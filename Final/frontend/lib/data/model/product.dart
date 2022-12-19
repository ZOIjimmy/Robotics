import 'dart:convert';

class Product {
  String name;
  String image;
  int rateNumber;
  String sources;
  int price;

  int? off;
  String about;
  bool isAvailable;
  int quantity;

  Product({
    required this.name,
    required this.image,
    required this.rateNumber,
    required this.sources,
    //
    required this.price,
    required this.about,
    required this.isAvailable,
    required this.off,
    required this.quantity,
  });

  Map<String, dynamic> toMap() => {
        "name": name,
        "image": image,
        "rateNumber": rateNumber,
        "sources": sources,
        "price": price,
        "about": about,
        "isAvailable": isAvailable,
        "off": off,
        "quantity": quantity,
      };

  factory Product.fromMap(Map<String, dynamic> map) {
    return Product(
      name: map['name'],
      image: map['image'],
      rateNumber: map['rateNumber'],
      sources: map['sources'],
      price: map['price'],
      about: map['about'],
      isAvailable: map['isAvailable'],
      off: map['off'],
      quantity: map['quantity'],
    );
  }

  String toJson() => json.encode(toMap());

  factory Product.fromJson(String source) =>
      Product.fromMap(json.decode(source));
}
