import 'package:flutter/material.dart';

class PreferenceFilter extends StatefulWidget {
  final Function(Map<String, dynamic>) onApply;

  const PreferenceFilter({super.key, required this.onApply});

  @override
  _PreferenceFilterState createState() => _PreferenceFilterState();
}

class _PreferenceFilterState extends State<PreferenceFilter> {
  final _minPriceController = TextEditingController(text: '100000');
  final _maxPriceController = TextEditingController(text: '500000');
  final _locationController = TextEditingController(text: 'Suburbs');
  int _minBedrooms = 2;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
        bottom: MediaQuery.of(context).viewInsets.bottom,
        left: 20,
        right: 20,
        top: 20,
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const Text(
            'Personalize Recommendations',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 20),
          TextField(
            controller: _minPriceController,
            decoration: const InputDecoration(labelText: 'Min Price (\$)'),
            keyboardType: TextInputType.number,
          ),
          TextField(
            controller: _maxPriceController,
            decoration: const InputDecoration(labelText: 'Max Price (\$)'),
            keyboardType: TextInputType.number,
          ),
          TextField(
            controller: _locationController,
            decoration: const InputDecoration(labelText: 'Preferred Location'),
          ),
          const SizedBox(height: 20),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Min Bedrooms'),
              DropdownButton<int>(
                value: _minBedrooms,
                items: [1, 2, 3, 4, 5].map((int value) {
                  return DropdownMenuItem<int>(
                    value: value,
                    child: Text('$value+'),
                  );
                }).toList(),
                onChanged: (value) {
                  setState(() {
                    _minBedrooms = value!;
                  });
                },
              ),
            ],
          ),
          const SizedBox(height: 30),
          ElevatedButton(
            onPressed: () {
              final prefs = {
                'min_price': double.tryParse(_minPriceController.text) ?? 0.0,
                'max_price': double.tryParse(_maxPriceController.text) ?? 1000000.0,
                'preferred_location': _locationController.text,
                'min_bedrooms': _minBedrooms,
              };
              widget.onApply(prefs);
              Navigator.pop(context);
            },
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 15),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
            ),
            child: const Text('Search Recommendations'),
          ),
          const SizedBox(height: 20),
        ],
      ),
    );
  }
}
