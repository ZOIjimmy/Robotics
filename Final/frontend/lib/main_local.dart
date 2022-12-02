import 'package:flutter/material.dart';
import 'package:frontend/environments/environment_singleton.dart';
import 'package:frontend/environments/local_config.dart';
import 'package:frontend/my_app.dart';

void main() async {
  Environment(baseConfig: LocalConfig());
  runApp(const MyApp());
}
