import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../widgets/user_tile.dart';
import '../providers/user_preview_provider.dart';
import '../providers/users_provider.dart';

class UsersGrid extends StatelessWidget {
  final bool likedByOnly, matchesOnly;

  UsersGrid(
    this.likedByOnly,
    this.matchesOnly
  );

  @override
  Widget build(BuildContext context) {
    final List<UserPreview> loadedUsers = likedByOnly
        ? Provider.of<Users>(context).likedBy
        : (matchesOnly ? Provider.of<Users>(context).matches : Provider.of<Users>(context).users);
    return GridView.builder(
      padding: const EdgeInsets.all(10),
      itemCount: loadedUsers.length,
      itemBuilder: (ctx, index) => ChangeNotifierProvider.value(
            //create: (ctx) => Products(), // use value if you don't need a builder
            value: loadedUsers[index],
            child: UserTile()),
      // FixedCrossAxis determines a strict colums number
      // FixedExtend determines element width and adjust columns accordingly
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 10,
        mainAxisSpacing: 10,
      ),
    );
  }
}
