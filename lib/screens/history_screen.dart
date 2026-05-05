import 'package:flutter/material.dart';
import '../models/message.dart';

class HistoryScreen extends StatefulWidget {
  final List<Message> history;

  const HistoryScreen({super.key, required this.history});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  late List<Message> history;

  @override
  void initState() {
    super.initState();
    history = widget.history;
  }

  void deleteMessage(int index) {
    setState(() {
      history.removeAt(index);
    });
  }

  String formatTime(DateTime time) {
    return "${time.day}/${time.month}/${time.year}  "
        "${time.hour}:${time.minute.toString().padLeft(2, '0')}";
  }

  void clearAll() {
    setState(() {
      history.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("History"),
        actions: [
          IconButton(
            icon: const Icon(Icons.delete_forever),
            onPressed: history.isEmpty ? null : clearAll,
          ),
        ],
      ),

      body: history.isEmpty
          ? const Center(child: Text("No history available"))
          : ListView.builder(
              itemCount: history.length,
              itemBuilder: (context, index) {
                final msg = history[index];

                return Card(
                  margin: const EdgeInsets.symmetric(
                    horizontal: 10,
                    vertical: 5,
                  ),
                  child: ListTile(
                    title: Text(msg.text),
                    subtitle: Text(formatTime(msg.time)),

                    trailing: IconButton(
                      icon: const Icon(Icons.delete, color: Colors.red),
                      onPressed: () {
                        showDialog(
                          context: context,
                          builder: (context) => AlertDialog(
                            title: const Text("Delete"),
                            content: const Text(
                              "Are you sure you want to delete this message?",
                            ),
                            actions: [
                              TextButton(
                                onPressed: () => Navigator.pop(context),
                                child: const Text("Cancel"),
                              ),
                              TextButton(
                                onPressed: () {
                                  deleteMessage(index);
                                  Navigator.pop(context);
                                },
                                child: const Text("Delete"),
                              ),
                            ],
                          ),
                        );
                      },
                    ),
                  ),
                );
              },
            ),
    );
  }
}
