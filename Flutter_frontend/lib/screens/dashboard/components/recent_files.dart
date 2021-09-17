import 'package:admin/models/RecentFile.dart';
import 'package:data_table_2/data_table_2.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';

import '../../../constants.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';


class RecentFiles extends StatelessWidget {
  const RecentFiles({
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(defaultPadding),
      decoration: BoxDecoration(
        color: secondaryColor,
        borderRadius: const BorderRadius.all(Radius.circular(10)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            "Последние оценки",
            style: Theme.of(context).textTheme.subtitle1,
          ),
         FutureBuilder<String?>(
                future: get("get_predictions"),
                builder: (BuildContext context, AsyncSnapshot<String?> snapshot) {
                  if (snapshot.hasData) {
                    final response = snapshot.data;
                    print("/////////////");
                    print(response);
                    print("/////////////");
                    final List t = json.decode(response!);
                    print(t);
                    final List<RecentFile> recentsList = t.map((item) => RecentFile.fromJson(item)).toList();
                    print(t);




                    return  SizedBox(
                        width: double.infinity,
                        child: DataTable2(
                      columnSpacing: defaultPadding,
                      minWidth: 600,
                      columns: [
                        DataColumn(
                          label: Text("Имя владельца"),
                        ),
                        DataColumn(
                          label: Text("Дата"),
                        ),
                        // DataColumn(
                        //   label: Text("Используемая модель"),
                        // ),
                        DataColumn(
                          label: Text("Предсказанная цена"),
                        ),
                      ],
                      rows: List.generate(
                        recentsList.length,
                        (index) => recentFileDataRow(recentsList[index]),
                      ),
                    ));
                  } else {
                    return Center(child: CircularProgressIndicator());
                  }
                }),
          
        ],
      ),
    );
  }
  Future<String?> get(String subject) async {
    var uri = Uri.parse("http://127.0.0.1:5000/" + subject);
    Map<String, String> headers = {"Content-type": "application/json"};
    try {
      var resp = await http.get(uri, headers: headers);
      //var resp=await http.get(Uri.parse("http://192.168.1.101:5000"));
      if (resp.statusCode == 200) {
        print("DATA FETCHED SUCCESSFULLY");
        var result = json.decode(resp.body);
        print("********");
        print(result);
        print("********");

        return result['response'];
      }
    } catch (e) {
      print("EXCEPTION OCCURRED: $e");
      return null;
    }
    return null;
  }
}

DataRow recentFileDataRow(RecentFile fileInfo) {
  return DataRow(
    cells: [
      DataCell(
        Row(
          children: [
            Container(
              padding: EdgeInsets.all(defaultPadding * 0.4),
              height: 30,
              width: 30,
              decoration: BoxDecoration(
                color: Colors.green.withOpacity(0.1),
                borderRadius: const BorderRadius.all(Radius.circular(10)),
              ),
              child: SvgPicture.asset(
                fileInfo.icon!,
                color: Colors.green,
              ),
            ),
            // SvgPicture.asset(
            //   fileInfo.icon!,
            //   height: 30,
            //   width: 30,
            // ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: defaultPadding),
              child: Text(fileInfo.name!),
            ),
          ],
        ),
      ),
      DataCell(Text(fileInfo.date!)),
      DataCell(Text(fileInfo.price!)),
    ],
  );
}
