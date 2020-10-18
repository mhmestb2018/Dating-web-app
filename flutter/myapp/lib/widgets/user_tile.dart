import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../providers/user_preview_provider.dart';
// import '../screens/product_details_screen.dart';
// import '../providers/cart_provider.dart';

class UserTile extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // the whole widget will not rebuild at any change
    final user = Provider.of<UserPreview>(context, listen: false);

    return ClipRRect(
      borderRadius: BorderRadius.circular(10),
      child: GestureDetector(
        // onTap: () => Navigator.of(context)
        //     .pushNamed(ProductDetailsScreen.route, arguments: product.id),
        child: GridTile(
          child: Image.network(
            user.pictures[0],
            fit: BoxFit.cover,
          ),
          footer: GridTileBar(
            backgroundColor: Colors.black87,
            title: Text(
              user.firstName,
              textAlign: TextAlign.center,
              softWrap: true,
            ),
            trailing: Icon(user.liked
                    ? Icons.favorite
                    : Icons.favorite_border,
              color: Theme.of(context).accentColor,
            )
          ),
        ),
      ),
    );
  }
}
