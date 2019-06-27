import csv

class ExportToCsv():
    def export_hw_csv(results):
        with open('exporthw.csv', mode='w') as csvfile:
            fieldnames = ['Serial number', 'CPU brand', 'CPU cores', 'CPU clock', 'RAM', 'Kernel version', 'macOS version', 'Hostname', 'Usernames']
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
            writer.writeheader()
            for i, j in results:
                writer.writerow(
                    {'Serial number': i.serial_number,
                    'CPU brand': i.cpu,
                    'CPU cores': i.cpu_cores,
                    'CPU clock': i.cpu_clock,
                    'RAM': i.ram,
                    'Kernel version': j.kernel_version,
                    'macOS version': j.os_version,
                    'Hostname': j.hostname,
                    'Usernames': j.usernames})
        return results

    def export_app_csv(results):
        with open('export_app.csv', mode='w') as csvfile:
            fieldnames = ['Serial number', 'Hostname', 'Application', 'Source', 'Last modified', 'Version']
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
            writer.writeheader()
            for i, j, l, k in results:
                writer.writerow(
                    {'Serial number': l.serial_number,
                    'Hostname': k.hostname,
                    'Application': i.application_name,
                    'Source': i.pkg_source,
                    'Last modified': i.last_modified,
                    'Version': j.version})
        return results
