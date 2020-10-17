import 'package:flutter/foundation.dart';
import 'package:meta/meta.dart';

class User with ChangeNotifier {
  final String firstName, lastName, bio, sex, orientation, password, email;
  final int validated, id;
  final double lat, lon;
  List<String> pictures;
  bool liked;

  User({
    @required this.firstName,
    @required this.lastName,
    @required this.password,
    @required this.email,
    @required this.id,
    this.bio = "J'aime manger des pommes",
    this.sex = "o",
    this.orientation = "bisexual",
    this.lat = 0.0,
    this.lon = 0.0,
    this.validated = 0,
    this.pictures
  });

  void toggleLiked() {
    liked = !liked;
    notifyListeners();
  }
}
