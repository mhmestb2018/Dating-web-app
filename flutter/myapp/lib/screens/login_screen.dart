import 'package:flutter/material.dart';
import 'package:requests/requests.dart';

import 'package:myapp/screens/users_overview_screen.dart';

class LoginScreen extends StatefulWidget {
  static const String route = '/login';

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {

  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [
              Colors.red,
              Colors.redAccent
            ],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter
          ),
        ),
        child: _isLoading ? Center(child: CircularProgressIndicator()) : ListView(
          children: <Widget>[
            headerSection(),
            fieldsSection(),
            buttonSection(),
          ]
        ),
      )
    );
  }

  login(String email, password) async {
    Map data = {
      'email': email,
      'password': password,
      'remember_me': true
    };
    var jsonData = null;
    var response = await Requests.post('http://0.0.0.0:5000/login', body: data);
    if (response.statusCode == 200) {
      jsonData = response.json();
      setState(() {
        _isLoading = false;
        Navigator.of(context).pushAndRemoveUntil(MaterialPageRoute(builder: (BuildContext context) => UsersOverviewScreen()), (route) => false);
      });
    }
    else {
      setState(() {
        _isLoading = false;
      });
      print(response.content());
    }
  }


  Container buttonSection() {
    return Container(
      width: MediaQuery.of(context).size.width,
      height: 40.0,
      padding: EdgeInsets.symmetric(horizontal: 20.0),
      margin: EdgeInsets.only(top: 30.0),
      child: RaisedButton(
        onPressed: () {
          setState(() {
            _isLoading = true;
          });
          login(emailController.text, passwordController.text);
        },
        child: Text("Sign in", style: TextStyle(color: Colors.white70)),
        color: Colors.purple,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(5.0))
      )
    );
  }

  TextEditingController emailController = new TextEditingController();
  TextEditingController passwordController = new TextEditingController();

  Container fieldsSection() {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 20.0),
      margin: EdgeInsets.only(top: 30.0),
      child: Column(children: [
        txtSection("Email", Icons.email, emailController),
        SizedBox(height: 30.0),
        txtSection("Password", Icons.lock, passwordController),
      ],)
    );
  }

  TextFormField txtSection(String title, IconData icon, TextEditingController controller) {
    return TextFormField(
      controller: controller,
      style: TextStyle(color: Colors.white70),
      decoration: InputDecoration(
        hintText: title,
        hintStyle: TextStyle(color: Colors.white70),
        icon: Icon(icon),
      ),
    );
  }

  Container headerSection() {
    return Container(
      padding: EdgeInsets.symmetric(
        horizontal: 20.0,
        vertical: 30.0,
      ),
      child: Text("Matchup", style: TextStyle(color: Colors.white))
    );
  }
}