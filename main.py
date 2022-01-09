from datetime import datetime
import ast
import os


class Entry:

    # Trying to read class variable counter
    try:
        with open("counter.txt", 'r', encoding="utf-8") as f:
            counter = int(f.read())
    except FileNotFoundError:
        with open("counter.txt", "w", encoding="utf-8") as f:
            counter = 0
            f.write(str(counter))

    def __init__(self, note, tags, id=0):

        # Update counter for ids of individual entries
        Entry.counter += 1
        if id > 0:
            Entry.counter -= 1
        with open("counter.txt", mode="w", encoding="utf-8") as f:
            f.write(str(Entry.counter))

        # Set entry data
        self.note = note
        self.tags = tags
        if id > 0:
            self.id = id
        else:
            self.id = Entry.counter
        self.time = datetime.now()

        # Save note locally as text file
        with open("notes.txt", mode="a", encoding="utf-8") as f:
            f.write(f'{{"id":{self.id},')
            f.write(f'"time":"{self.time}",')
            f.write(f'"note":"{self.note}",')
            f.write(f'"tags":{self.tags}}}')
            f.write("\n")

        # Notification that new entry was created successfully.
        print(f"\nCreated new entry with id {self.id}\n")

    def get_all_entries():
        """
           Method that reads all notes and returns them as a list.
           Returns List<Entry>
        """
        all_entries = []
        with open("notes.txt", mode="r", encoding="utf-8") as f:
            for line in f:
                entry = ast.literal_eval(line)
                all_entries.append(entry)
        return all_entries

    def get_all_tags():
        """
           Method that returns all tags used.
           Returns Set<Tag>
        """
        tags = []
        all_entries = Entry.get_all_entries()
        for entry in all_entries:
            tags.extend(entry["tags"])
        return set(tags)

    def get_entries_by_tag(tag):
        return_entries = []
        all_entries = Entry.get_all_entries()
        for entry in all_entries:
            if tag in entry["tags"]:
                return_entries.append(entry)
        return return_entries


if __name__ == "__main__":

    while True:
        print("\nMENU")
        print("\n0 Clear screen\n1 Create Entry\n2 Print Entries\n3 Show Entries By Tag\n4 Edit Entry\n5 Delete Entry\n6 Reset application")
        print("Q Quit Application\n")

        user_input = input("What's up next? ")

        if user_input == 'Q' or user_input == 'q' or user_input == "bye":
            print("\nBye, see you next time!\n")
            break

        elif user_input == "0":
            """Clean screen."""
            os.system('cls' if os.name == 'nt' else 'clear')

        elif user_input == "1":
            """Create a new entry."""
            note = input("Your new note: ")
            tag_input = input("Tags (separated by commas): ")
            tags_split = tag_input.split(',')
            tags = []
            for tag in tags_split:
                tags.append(tag.strip())
            entry = Entry(note=note, tags=tags)

        elif user_input == "2":
            """Print all existing notes to screen."""
            all_entries = []
            try:
                all_entries = Entry.get_all_entries()
            except FileNotFoundError:
                print("Missing File: No entries yet.")
            else:
                if all_entries:
                    for entry in all_entries:
                        print(entry)
                else:
                    print("No entries yet.")

        elif user_input == "3":
            """Show entries filtered by tag."""
            while True:
                all_tags = Entry.get_all_tags()
                print(f"\nTags in use: {all_tags}")
                tag_choice = input("\nChoose tag for look up (Q for quit): ")
                if tag_choice == 'Q' or tag_choice == 'q':
                    break
                entries = Entry.get_entries_by_tag(tag_choice)
                if entries: 
                    for entry in entries:
                        print(entry)
                else:
                    print("No matches found") 

        elif user_input == "4":
            """Edit existing entry."""
            all_entries = Entry.get_all_entries()
            for entry in all_entries:
                print(entry)

            # Defining ID of entry to be overwritten 
            while True:
                entry_choice = input("\nWrite id of entry you want to edit (Q for quit): ")
                if entry_choice == 'q' or entry_choice == 'Q':
                    break
                entry_choice_int = int(entry_choice)    
                entry_backup = dict()
                with open("notes.txt", "w") as f:
                    for entry in all_entries:
                        if entry_choice_int != entry["id"]:
                            f.write(str(entry))
                            f.write("\n")
                        else:
                            entry_backup = entry

                if len(entry_backup) == 0:
                    print("No match found")
                    continue

                # Creating new entry for id == entry_choice
                print(f"You are overwriting {entry_backup}")
                note = input("Your new note: ")
                tag_input = input("Tags (separated by commas): ")
                tags_split = tag_input.split(',')
                tags = []
                for tag in tags_split:
                    tags.append(tag.strip())
                entry = Entry(note=note, tags=tags, id=entry_choice_int)
                break

        elif user_input == "5":
            all_entries = Entry.get_all_entries()
            for entry in all_entries:
                print(entry)

            # Defining ID of entry to be deleted 
            entry_choice = input("\nWrite id of entry you want to delete (Q for quit): ")
            if entry_choice == 'q' or entry_choice == 'Q':
                break
            entry_choice = int(entry_choice)    

            with open("notes.txt", "w") as f:
                for entry in all_entries:
                    if entry_choice != entry["id"]:
                        f.write(str(entry))
                        f.write("\n")

        elif user_input == "6":
            print("You are about to delete all entries.")
            user_decision = input("Are you sure to continue [Y/y]? ")
            if user_decision == 'Y' or user_decision == 'y':
                with open("counter.txt", mode="w", encoding="utf-8") as f:
                    f.write("0")
                with open("notes.txt", mode="w", encoding="utf-8") as f:
                    f.write("")

        else:
            continue

os.system('cls' if os.name == 'nt' else 'clear')
