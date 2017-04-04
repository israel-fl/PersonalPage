function filterByOrg(group, id, orgs) {
    var holder = document.getElementById(id);
    for (org in orgs) {
        if (orgs[org].name == group) {
            var mach_dict = orgs[org].agents;
        }
    }
    while (holder.firstChild) {
        holder.removeChild(holder.firstChild);
    }
    var empty = document.createElement('option');
    holder.add(empty);
    for (mach in mach_dict) {
        var input = document.createElement('option');

        if (id == 'machine-dropdown-list') {
            input.setAttribute("id", 'backup' + mach_dict[mach].name);
            holder.setAttribute("onchange", "getAgentGuid(this.value, " + mach_dict[mach].guid + ")");
        } else if (id == 'ret-machine-dropdown-list') {
            input.setAttribute("id", 'ret' + mach_dict[mach].name);
            holder.setAttribute("onchange", "filterByMachine(this.value, 'archive-dropdown-list', " + JSON.stringify(mach_dict[mach]) + ")");
        } else if (id == 'view-machine-dropdown-list') {
            input.setAttribute("id", 'view' + mach_dict[mach].name);
            // holder.setAttribute("onchange", "displayDetails(" + JSON.stringify(mach_dict[mach]) + ")");
        } else if (id == 'remove-machine-dropdown-list') {
            input.setAttribute("id", 'remove' + mach_dict[mach].name);
            holder.setAttribute("onchange", "getAgentGuid(this.value, " + mach_dict[mach].guid + ")");
        }
        input.setAttribute("value", mach_dict[mach].name);
        input.innerHTML = mach_dict[mach].name;
        holder.add(input);
    }
}


function filterByMachine(value, id, machine) {

    var holder = document.getElementById(id);
    while (holder.firstChild) {
        holder.removeChild(holder.firstChild);
    }

    var archives = machine.archives;

    var hiddenAgentGuid = document.getElementById('agent-guid');
    hiddenAgentGuid.setAttribute("name", "agent-guid");
    hiddenAgentGuid.setAttribute("value", machine.guid);
    // Get all of the archives that belong to and agent
    for (arch in archives) {
        var input = document.createElement('option');
        input.setAttribute("id", archives[arch].name);
        input.setAttribute("value", archives[arch].id);
        input.innerHTML = archives[arch].created;
        holder.add(input);
    }
    holder.setAttribute("onchange", "setChosenArchive()")
}


function getAgentGuid(machine, guid) {
    var input = document.getElementById('selectedbackup');
    input.setAttribute("value", guid);
}


// function displayDetails(machine) {
//     table = document.getElementById("archives");
//     archive_details = machine.archives;
//     for (archive in archive_details) {
//         var row = table.insertRow()
//         var date = row.insertCell(0);
//         var archiveID = row.insertCell(1);
//         date.innerHTML = archive_details[archive].date;
//         archiveID.innerHTML = archive_details[archive].name;
//     }
// }
