import 'package:admin/responsive.dart';
import 'package:admin/screens/dashboard/components/my_fields.dart';
import 'package:flutter/material.dart';

import '../../constants.dart';
import 'components/header.dart';

import 'components/recent_files.dart';
import 'components/storage_details.dart';


int predictionItems = 2;


class DashboardScreen extends StatefulWidget {

  DashboardScreen({Key? key}) : super(key: key);

  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}
class Data{
  List<bool> isChecked = List.filled(predictionItems, false);
  List<String> predictions = List.filled(predictionItems, "");
}
class _DashboardScreenState extends State<DashboardScreen> {

  late Widget generalView = Row(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Expanded(
        child: Column(
          children: [
            MyFiles(callback: callback, data: data,),
            SizedBox(height: defaultPadding),
            RecentFiles(),
            if (Responsive.isMobile(context))
              SizedBox(height: defaultPadding),
            // if (Responsive.isMobile(context)) StorageDetails(),
          ],
        ),
      ),
      if (!Responsive.isMobile(context))
        SizedBox(width: defaultPadding),
      // On Mobile means if the screen is less than 850 we dont want to show it
      // if (!Responsive.isMobile(context))
      //   Expanded(
      //     flex: 2,
      //     child: StorageDetails(),
      //   ),
    ],
  );
  late Widget currentPage = generalView;
  late Data data;

  @override
  void initState() {
    super.initState();
    data = Data();
  }

  void callback(Widget nextPage, Data data) {
    setState(() {
      this.currentPage = nextPage;
      this.data = data;
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: SingleChildScrollView(

        padding: EdgeInsets.all(defaultPadding),
        child: Column(
          children: [
            Header(),
            SizedBox(height: defaultPadding),
            currentPage,
          ],
        ),
      ),
    );
  }
}


