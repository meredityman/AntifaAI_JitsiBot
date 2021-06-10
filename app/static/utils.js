

class UserList {
  constructor(element, participants, selectionChangedCallback) {
      this.element      = element;
      this.selectionChangedCallback = selectionChangedCallback;


      this.participants = participants;

      this.listEl = $('<ul id="user-list-ul"></ul>');
      this.element.append(this.listEl);

      this.participants.array.forEach(element => {
        let button = this.addButton(element.displayName, element.id, element.selected);
        button = button.wrap('<li class="list-group-item"></li>').parent();
        this.listEl.append(button);
      });

  };

  addButton(displayName, uid, selected){
    let text = displayName + " (" + uid + ")";
    let id = 'user-btn-' + uid

    function callback(){
        if(id in self.participants){
            participants[id]['selected'] = !participants[uid]['selected']
            $( this ).toggleClass( "selected" );
            self.selectionChangedCallback( {'ids': getSelectedUsers()});
        } else {
            console.error("No participant for button (" + uid +")");
            console.error(participants);
        };
    }

    return $('<button/>', {
        text: text, 
        id: id,
        class : 'user-btn',
        click: callback
    });
  }

  addUser( user, displayName, selected = false){
    console.log("Adding user " + id);
    participants[id] = {
        'displayName' : displayName,
        'messages' : [],
        'selected' : selected
      };
  };

  removeUser( user){
    console.log("Removing user " + id);
    delete participants[id];
    $('#user-btn-' + id).parent().remove();
  };

};