import 'package:flutter/material.dart';
import 'package:frontend/environments/environment_singleton.dart';
import 'package:frontend/environments/local_config.dart';
import 'package:frontend/init_service.dart';
import 'package:frontend/my_app.dart';

void main() async {
  Environment(baseConfig: LocalConfig());

  await setupService();

  runApp(const MyApp());
}
