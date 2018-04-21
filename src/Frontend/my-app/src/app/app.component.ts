import { Component } from '@angular/core';
import { HostListener } from '@angular/core';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'your DOOOOOOOOOOM';
  text = '';
  kek = '';

  setText(text) {
    this.text = text;
  }

  @HostListener('document:keypress', ['$event'])
  handleKeyboardEvent(event: KeyboardEvent) {
    if (event.keyCode == 13) {
      this.kek = document.getElementById("asdf").value;
    } else {
      this.kek = '';
    }
  }
}
