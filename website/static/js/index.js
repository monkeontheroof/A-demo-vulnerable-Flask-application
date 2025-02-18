function deleteNote(noteId) {
    fetch("/delete-note/"+noteId, {
      method: "POST",}).then((_res) => {
        window.location.reload();
    });
  }
