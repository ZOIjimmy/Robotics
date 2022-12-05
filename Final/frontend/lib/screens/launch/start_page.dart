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

  AnimationController? _controller;
  bool _isAnimationEnd = false;
  int cont = 0;
  int targetCount = 3;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(vsync: this);
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.amber,
      body: Center(
        child: Stack(
          alignment: Alignment.center,
          children: [_buildOpacityImageLogo(), _buildLottie(context)],
        ),
      ),
    );
    // _buildLaunchEventListener()
  }

  Widget _buildOpacityImageLogo() {
    return AnimatedOpacity(
      opacity: _isAnimationEnd ? 1 : 0,
      duration: const Duration(milliseconds: 1000),
      onEnd: () => {},
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

  Widget _buildLottie(BuildContext context) {
    if (_isAnimationEnd) {
      return const SizedBox.shrink();
    }

    final controller = _controller;
    if (controller == null) {
      return const SizedBox.shrink();
    }

    _controller?.addStatusListener((status) {
      if (status == AnimationStatus.completed) {
        // print('Animation ${cont + 1} completed. ');
        cont++;
        if (cont < targetCount) {
          _controller!.reset();
          _controller!.forward();
        } else {
          setState(() {
            _isAnimationEnd = true;
          });
        }
      }
    });

    return Lottie.asset(LottieAsset.startLottie,
        width: _sizeLaunchIcon,
        height: _sizeLaunchIcon,
        controller: controller, onLoaded: (composition) {
      controller
        ..duration = composition.duration
        ..forward();
    });
  }
}
