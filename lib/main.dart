import 'package:flutter/material.dart';
import 'screens/dashboard_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  bool isDarkMode = true;
  String appName = "Desktop Companion";

  // 🔹 Toggle Theme
  void toggleTheme(bool value) {
    setState(() {
      isDarkMode = value;
    });
  }

  // 🔹 Update App Name
  void updateAppName(String name) {
    setState(() {
      appName = name;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: appName,

      // 🔹 Dynamic Theme
      theme: isDarkMode ? ThemeData.dark() : ThemeData.light(),

      // 🔹 Pass data to Dashboard
      home: DashboardScreen(
        isDarkMode: isDarkMode,
        onThemeChanged: toggleTheme,
        appName: appName,
        onNameChanged: updateAppName,
      ),
    );
  }
}
