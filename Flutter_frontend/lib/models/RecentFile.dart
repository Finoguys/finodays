class RecentFile {
  final String? icon, name, date, price;

  RecentFile({this.icon, this.name, this.date, this.price});

  factory RecentFile.fromJson(Map<String, dynamic> json) {
    return RecentFile(
      icon: "assets/icons/camera.svg",
      name: json['name'],
        date: json['date'],
        price: json['price'],
    );
  }
}

List demoRecentFiles = [
  RecentFile(
    icon: "assets/icons/camera.svg",
    name: "Иван Пупочкин",
    date: "01-03-2021",
    price: "300\$",
  ),

];
