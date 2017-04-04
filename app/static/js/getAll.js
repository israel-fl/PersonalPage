function filterAll(value, id, all_orgs, managed_orgs) {
    var holder = document.getElementById(id);
    while (holder.firstChild) {
        holder.removeChild(holder.firstChild);
    }
    var hiddenID = document.getElementById('selected-org-id');
    for (org in managed_orgs) {
        if (managed_orgs[org].name == value) {
            hiddenID.setAttribute("value", managed_orgs[org].id)
        }
    }
    for (org in all_orgs) {
        if (all_orgs[org].name == value) {
            var mach_dict = all_orgs[org].agents;
        }
    }
    var empty = document.createElement('option');
    holder.add(empty);
    for (var mach in mach_dict){
        var input = document.createElement('option');
        input.setAttribute("value", mach_dict[mach].name);
        holder.setAttribute("onchange", "configureNewAgent(" + mach_dict[mach].guid + ")");
        input.innerHTML = mach_dict[mach].name;
        input.setAttribute("id", 'add' + mach_dict[mach].name);
        holder.add(input);
    }
}

function configureNewAgent(guid){
    var hiddenAgentGuid = document.getElementById('agent-guid-configure');
    hiddenAgentGuid.setAttribute("value", guid)
}
