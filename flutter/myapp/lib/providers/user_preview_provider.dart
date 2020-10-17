import 'package:flutter/foundation.dart';
import 'package:meta/meta.dart';

class UserPreview with ChangeNotifier {
  final String firstName;//, sex, orientation;
  final int age, id;
  // final double lat, lon;
  List<String> pictures;
  bool liked, matches, blocked;

  UserPreview({
    @required this.firstName,
    @required this.id,
    this.liked = false,
    this.matches = false,
    this.blocked = false,
    // this.sex = "o",
    this.age = 18,
    // this.orientation = "bisexual",
    // this.lastSeen = 0.0,
    // this.lat =0.0,
    // this.lon = 0.0,
    // this.validated = 0,
    this.pictures
  });

  void toggleLiked() {
    liked = !liked;
    notifyListeners();
  }
}
