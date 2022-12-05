import 'package:flutter/material.dart';

class CustomTextBox extends StatelessWidget {
  CustomTextBox(
      {Key? key, this.hint = "", this.prefix, this.suffix, this.controller})
      : super(key: key);
  final String hint;
  final Widget? prefix;
  final Widget? suffix;
  final TextEditingController? controller;
  @override
  Widget build(BuildContext context) {
    return Container(
      alignment: Alignment.center,
      padding: EdgeInsets.only(bottom: 3),
      height: 44,
      decoration: BoxDecoration(
          color: Colors.white,
          border: Border.all(color: Colors.black),
          borderRadius: BorderRadius.circular(10)),
      child: TextField(
        controller: controller,
        decoration: InputDecoration(
            prefixIcon: prefix,
            suffixIcon: suffix,
            border: InputBorder.none,
            hintText: hint,
            hintStyle: TextStyle(color: Colors.black, fontSize: 15)),
      ),
    );
  }
}
