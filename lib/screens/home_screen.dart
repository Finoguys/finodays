import 'package:finodays_website/widgets/action_button.dart';
import 'package:finodays_website/widgets/centered_view.dart';
import 'package:finodays_website/widgets/course_details.dart';
import 'package:finodays_website/widgets/navigation_bar.dart';
import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: CenteredView(
        child: Column(
          children: <Widget>[
            NavigationBar(),
            Expanded(
              child: Row(children: [
                CourseDetails(),
                Expanded(
                  child: Center(
                    child: ActionButton('Join Course'),
                  ),
                )
              ]),
            )
          ],
        ),
      ),
    );
  }
}
