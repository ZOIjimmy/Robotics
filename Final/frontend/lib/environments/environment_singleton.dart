import 'base_config.dart';

class Environment {
  Environment._internal();

  static final Environment _singleton = Environment._internal();

  late BaseConfig config;

  factory Environment({BaseConfig? baseConfig}) {
    if (baseConfig != null) {
      _singleton.config = baseConfig;
    }
    return _singleton;
  }
}
