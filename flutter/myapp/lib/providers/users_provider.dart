import 'package:flutter/foundation.dart';

import './user_preview_provider.dart';
import '../dummies.dart';

class Users with ChangeNotifier {
  List<UserPreview> _users = dummyUsersList;
  
  // // Could be a global state management
  // var _favoriteOnly = false;

  // void toggleFavoritesFilter() {
  //   _favoriteOnly = !_favoriteOnly;
  //   notifyListeners();
  // }

  // set favoritesFilter(bool value) {
  //   _favoriteOnly = value;
  //   notifyListeners();
  // }

  List<UserPreview> get users {
    return [..._users];
  }

  List<UserPreview> get likedBy {
    return [..._users];
  }

  List<UserPreview> get matches {
    return [..._users];
  }

  UserPreview findById(int id) {
    return _users.firstWhere((user) => user.id == id);
  }

  void addUser(value) {
    _users.add(value);
    notifyListeners();
  }
}