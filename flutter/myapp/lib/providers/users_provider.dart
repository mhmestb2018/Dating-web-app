import 'package:flutter/foundation.dart';
import 'package:requests/requests.dart';

import './user_preview_provider.dart';
import '../dummies.dart';

class Users with ChangeNotifier {
  List<UserPreview> _dusers = dummyUsersList;

  List<UserPreview> get users {
    List<UserPreview> _users;
    Requests.post('http://localhost:5000/users').then((response) {
      response.json().forEach((elem) {
        _users.add(
          UserPreview(
            firstName: elem["first_name"],
            id: elem["id"],
            age: elem["age"],
            blocked: elem["blocked"],
            liked: elem["liked"],
            matches: elem["matches"],
            pictures: elem["pictures"]
          )
        );
      });
    }).catchError((error) => log.shout(error));
    return _users;
  }

  List<UserPreview> get likedBy {
    return [..._dusers];
  }

  List<UserPreview> get matches {
    return [..._dusers];
  }
}