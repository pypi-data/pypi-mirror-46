#
#   Copyright (c) 2018 Daniel Schmitz
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.

from prometheus_client import Gauge


class metric:
    def __init__(self, name, value=None, description=None):
        self.name = name
        if description is None:
            description = name.replace('_', ' ')
        self.metric = Gauge(name.lower(), description)
        if not value is None:
            self.value = value
            self.metric.set(value)

    def update(self, value):
        self.value = value
        self.metric.set(value)

    # Delete
    def update_value(self, value):
        self.update(value)

    def get_value(self):
        return self.value


class metric_label:
    def __init__(self, name, label, value=None, description=None):
        self.name = name
        self.values = dict()
        self.label_values = list()
        self.label = label
        if description is None:
            description = name.replace('_', ' ')
        self.metric = Gauge(name.lower(), description, [label])
        if not value is None:
            self.metric.labels(label).set(value)

    def update(self, value):
        removable_labels = list()
        for label in value:
            self.values[label] = value[label]
            self.metric.labels(label).set(value[label])
            if label not in self.label_values:
                self.label_values.append(label)
        for label in self.label_values:
            if not label in value:
                self.metric.labels(label).set(0)
                self.values[label] = 0
            if self.values[label] < 1:
                removable_labels.append(label)
        for l in removable_labels:
            self.metric.remove(label)
            del(self.values[l])

    # Delete
    def update_value(self, value):
        self.update_value(value)
        removable_labels = list()

    def get_value(self):
        return self.values

    def get_label_values(self):
        return self.label_values

    def get_label(self):
        return self.label


class metric_labels:
    def __init__(self, name, labels, values=None, description=None):
        self.name = name
        self.values = dict()
        self.labels = labels
        if description is None:
            description = name.replace('_', ' ')
        self.metric = Gauge(name.lower(), description, labels)
        if not values is None:
            self.update(values)

    def __zero_missing_value(self, value):
        if isinstance(value, dict):
            for label in values:
                value[label] = self.__zero_missing_value(value[label])
        else:
            value = 0
        return value

    def __remove_empty_values(self, values):
        removeable_values = list()
        if isinstance(values, dict):
            for label in values:
                print(label)
                if not isinstance(values[label], dict):
                    if values[label] < 1:
                        removeable_values.append(label)
                else:
                    values[label] = self.__remove_empty_values(values[label])
                    if not values[label]:
                        removeable_values.append(label)
        for labels in removeable_values:
            del values[label]
        return values

    def __remove_empty_label_sets(self, values, labels=None):
        #print(values)
        if not labels:
            labels = list()
        if isinstance(values, dict):
            for label in values:
                labels_new = labels.copy()
                labels_new.append(label)
                self.__remove_empty_label_sets(values[label], labels_new)
        else:
            print("values: %s" % values)
            if values < 1:
                print("labels: %s" % labels)
                print(len(labels))
                print(len(self.metric._labelnames))
                self.metric.remove(*labels)

    def __update_old_values(self, old_values, values):
        for label in old_values:
            if not label in values:
                old_values[label] = self.__zero_missing_value(
                    old_values[label])
            else:
                if isinstance(old_values[label], dict):
                    old_values[label] = self.__update_old_values(
                        old_values[label], values[label])
        return old_values

    def __add_new_values(self, old_values, values):

        for label in values:
            if not isinstance(values[label], dict):
                old_values[label] = values[label]
            else:
                if label in old_values:
                    old_values[label] = self.__add_new_values(
                        old_values[label], values[label])
                else:
                    old_values[label] = values[label]

        return old_values

    def __update_metrics(self, values, labels=None):
        for label in values:
            labels_tmp = list()
            if not labels is None:
                for i in labels:
                    labels_tmp.append(i)
            labels_tmp.append(label)

            if not isinstance(values[label], dict):
                self.metric.labels(*labels_tmp).set(values[label])
                labels_tmp.pop()
            else:
                self.__update_metrics(values[label], labels_tmp)

    def __add_value_dict(self, d, items, value):
        if len(items) > 1:
            if not items[0] in d:
                d[items[0]] = dict()
            current = items[0]
            items.pop(0)
            d[current] = self.__add_value_dict(d[current], items, value)
        else:
            d[items[0]] = value
        return d

    def get_value(self):
        return self.values

    def get_name(self):
        return self.name

    def get_labels(self):
        return self.labels

    def update(self, values):
        if isinstance(values, list):
            values_new = dict()
            for v in values:
                v_temp = v[:len(v) - 1]
                metric_value = v[len(v) - 1]
                values_new = self.__add_value_dict(values_new, v_temp,
                                                   metric_value)
                values = values_new
        self.values = self.__add_new_values(self.values, values)
        self.values = self.__update_old_values(self.values, values)
        self.__remove_empty_label_sets(self.values)
        self.values = self.__remove_empty_values(self.values)
        self.__update_metrics(self.values)

    # Delete
    def update_value(self, value):
        self.update(value)
