
next_column = len(all_entries)

ent = Entry(frame_for_boxes)
ent.grid(row=0, column=next_column)

all_entries.append( ent )



exec("try: \n \t next_column = len(all_entries) \n \t ent = Entry(frame_for_boxes) \n \t ent.grid(row=0, column=next_column) \n \t all_entries.append( ent ) \nexcept: pass")