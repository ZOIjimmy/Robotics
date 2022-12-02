import 'package:frontend/const/lottie_asset.dart';
import 'package:lottie/lottie.dart';
import 'package:flutter/material.dart';
import 'package:frontend/const/image_asset.dart';

class StartPage extends StatefulWidget {
  static const String tag = 'tag';
  const StartPage({Key? key}) : super(key: key);

  @override
  State<StartPage> createState() => _StartPageState();
}

class _StartPageState extends State<StartPage> with TickerProviderStateMixin {
  static const double _sizeLaunchIcon = 300;

  AnimationController? _catBoxController;
  bool _isCatBoxAnimationEnd = false;

  @override
  void initState() {
    super.initState();

    _catBoxController = AnimationController(vsync: this);
  }

  @override
  void dispose() {
    _catBoxController?.dispose();
    super.dispose();
  }

  // return Scaffold(
  //   body: child,
  //   backgroundColor: Colors.amber,
  // );

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Stack(
        alignment: Alignment.center,
        children: [_buildOpacityImageLogo(), _buildLottieCatBox(context)],
      ),
    );
    // _buildLaunchEventListener()
  }

  Widget _buildOpacityImageLogo() {
    return Opacity(
      opacity: _isCatBoxAnimationEnd ? 1 : 0,
      child: Hero(
        tag: StartPage.tag,
        child: Image.asset(
          ImageAsset.startIcon,
          width: _sizeLaunchIcon,
          height: _sizeLaunchIcon,
        ),
      ),
    );
  }

  Widget _buildLottieCatBox(BuildContext context) {
    if (_isCatBoxAnimationEnd) {
      return const SizedBox.shrink();
    }

    final controller = _catBoxController;
    if (controller == null) {
      return const SizedBox.shrink();
    }

    _catBoxController?.addStatusListener((status) {
      if (status == AnimationStatus.completed) {
        setState(() {
          _isCatBoxAnimationEnd = true;
        });
      }
    });

    return Lottie.asset(LottieAsset.startLottie,
        width: _sizeLaunchIcon,
        height: _sizeLaunchIcon,
        controller: controller, onLoaded: (composition) {
      controller
        ..duration = composition.duration
        ..forward();
      // ..repeat(max: 3, period: composition.duration * 2);
    });
  }
}
