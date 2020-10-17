import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import './screens/users_overview_screen.dart';
import './screens/login_screen.dart';
// import './screens/product_details_screen.dart';
// import './providers/products_provider.dart';
import './providers/users_provider.dart';
// import './screens/cart_screen.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    //create: (ctx) => Products(), // use value if you don't need a builder
    return MultiProvider(
      providers: [
        ChangeNotifierProvider.value(value: Users()),
        // ChangeNotifierProvider.value(value: Cart()),
      ],
      child: MaterialApp(
        title: 'MatchUp',
        theme: ThemeData(
            primarySwatch: Colors.red,
            accentColor: Colors.redAccent,
            fontFamily: 'Lato'),
        home: LoginScreen(),
        routes: {
          UsersOverviewScreen.route: (ctx) => UsersOverviewScreen(),
          LoginScreen.route: (ctx) => LoginScreen(),
        },
      ),
    );
  }
}
