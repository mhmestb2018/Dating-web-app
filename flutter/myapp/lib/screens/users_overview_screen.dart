import 'package:flutter/material.dart';
import 'package:myapp/providers/user_preview_provider.dart';
import 'package:provider/provider.dart';

// import '../widgets/products_grid.dart';
import '../widgets/users_grid.dart';
import '../providers/users_provider.dart';
// import '../screens/cart_screen.dart';

enum FilterOptions {
  LikedBy,
  Matches,
  All,
}

class UsersOverviewScreen extends StatefulWidget {
  static const String route = '/users';

  @override
  _UsersOverviewScreenState createState() => _UsersOverviewScreenState();
}

class _UsersOverviewScreenState extends State<UsersOverviewScreen> {
  bool _likedByOnly = false;
  bool _matchesOnly = false;

  @override
  Widget build(BuildContext context) {
    final users = Provider.of<Users>(context, listen: false);
    return Scaffold(
      appBar: AppBar(
        title: Text('Matchup'),
        actions: <Widget>[
          PopupMenuButton(
            icon: Icon(Icons.more_vert),
            onSelected: (FilterOptions selectedValue) {
              setState(() {
                switch (selectedValue) {
                  case FilterOptions.All:
                    {
                      _likedByOnly = false;
                      _matchesOnly = false;
                      break;
                    }
                  case FilterOptions.LikedBy:
                    {
                      _likedByOnly = true;
                      _matchesOnly = false;
                      break;
                    }
                  case FilterOptions.Matches:
                    {
                      _matchesOnly = true;
                      _likedByOnly = false;
                      break;
                    }
                }
              });
            },
            itemBuilder: (_) => [
              PopupMenuItem(
                child: const Text('All Users'),
                value: FilterOptions.All,
              ),
              PopupMenuItem(
                child: const Text('Liked By'),
                value: FilterOptions.LikedBy,
              ),
              PopupMenuItem(
                child: const Text('Matches'),
                value: FilterOptions.LikedBy,
              ),
            ],
          ),
        ],
      ),
      body: UsersGrid(_likedByOnly, _matchesOnly),
    );
  }
}
