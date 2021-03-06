from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Summary, Entry, Report, Item
from fileuploads.models import Video
from groups.models import Process, Result, Row
from signals.models import Process as File_Process, Output, Signal
from policies.models import Policy, Operation

from django.contrib.auth.decorators import login_required


@login_required(login_url="/login/")
def dashboard(request):
    return render(request, 'reports/dashboard.html')


def create_entry(process, summary):
    values_dict = {}
    results = Result.objects.filter(process=process)
    entries = []

    for result in results:
        rows = Row.objects.filter(result=result)
        video = Video.objects.get(filename=result.filename)
        if video.frame_count == 0:
            video.frame_count = rows[0].frame_number
            video.save()

        for row in rows:
            if row.op_id in values_dict:
                ls = values_dict[row.op_id]
                ls.append((result.filename, row.result_number))
            else:
                values_dict[row.op_id] = [(result.filename, row.result_number)]

    for op_id, ls in values_dict.items():
        op = Operation.objects.get(id=op_id)
        percentage = op.percentage
        nums = []
        for item in ls:
            nums.append(item[1])
        average = sum(nums)/len(nums)

        for item in ls:
            if percentage == 0.0:
                continue
            if average == 0:
                average = 1
            if ((item[1] - average)/average) * 100 > percentage:
                new_entry = Entry(
                    summary=summary,
                    file_name=item[0],
                    operation_id=op_id,
                    operation_name=op.op_name,
                    signal_name=op.signal_name,
                    second_signal_name=op.second_signal_name,
                    percentage=percentage,
                    result_number=item[1],
                    average=average,
                    cut_off=op.cut_off_number
                )
                new_entry.save()


def get_off_values(high, low, values, times):
    off_values = []
    off_times = []
    index = 0
    while index < len(values):
        value = values[index]
        time = times[index]
        if value >= high:
            off_values.append(value)
            off_times.append(time)
        elif value <= low:
            off_values.append(value)
            off_times.append(time)
        index += 1
    off_values.sort()
    off_times.sort()
    return (off_values, off_times)


def create_item(process, report):
    values_dict = {}
    outputs = Output.objects.filter(process=process)

    for output in outputs:
        items, values, times, percentages = [], [], [], []
        #output has only one signal type but signal could have multiple entries
        signals = Signal.objects.filter(output=output)
        for signal in signals:
            values += signal.signal_values
            times += signal.frame_times
        if len(values) == 0:
            continue
        average = sum(values)/len(values)
        # find parcentages it would need to generate items
        # it checks against average
        policy = Policy.objects.get(id=process.policy_id)
        temp_operations = Operation.objects.filter(policy=policy)
        operations = temp_operations.filter(signal_name=output.signal_name)

        for op in operations:
            if op.file_percentage > 0:
                percentages.append(op.file_percentage)

        percentages.sort()
        op_id = operations[0].pk
        op = Operation.objects.get(id=op_id)

        for per in percentages:
            if per > 100:
                high = average * (per/100)
                low = average - average*(per/100)
            else:
                high = average + average*(per/100)
                low = average - average*(per/100)
            results = get_off_values(high, low, values, times)
            key = str(per) + output.signal_name
            new_item = Item(
                report=report,
                file_name=process.file_name,
                signal_name=op.get_signal_name_display,
                op_id=op.pk,
                total_frame_number=process.frame_count,
                off_total_frame_number=len(results[0]),
                percentage=per,
                off_signal_values=results[0],
                off_frame_times=results[1],
                average=average
            )
            new_item.save()
            if len(values) == 0:
                break


def create_summary(process):
    summary = Summary.objects.filter(process_id=process.id)
    if summary.count() > 0:
        return summary[0]
    else:
        new_summary = Summary(
            user_name=process.user_name,
            process_id=process.id,
            policy_name=process.policy_name,
            policy_id=process.policy_id,
            group_id=process.group_id,
            group_name=process.group_name,
        )
        new_summary.save()
        create_entry(process, new_summary)
        return new_summary


def create_report(process):
    report = Report.objects.filter(process_id=process.id)
    video = Video.objects.get(filename=process.file_name)
    if video.frame_count == 0:
        video.frame_count = process.frame_count
        video.save()

    if report.count() > 0:
        return report[0]
    else:
        new_report = Report(
            user_name=process.user_name,
            process_id=process.id,
            policy_name=process.policy_name,
            policy_id=process.policy_id,
            file_id=process.file_id,
            file_name=process.file_name,
        )
        new_report.save()
        create_item(process, new_report)
        return new_report
