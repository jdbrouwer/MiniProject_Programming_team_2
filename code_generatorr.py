name = input("what is your name")
mail = input("what is your mail")
film = input("whats is the movie")
starttijd = input("time 1")

def codegenerator(name, mail, film, starttijd):
    """
 this function makes from the name, mail, film and starttijd a code
    """
    gen_name = []
    for c in name:
        shift = ord(c) + 4
        change = chr(shift)
        gen_name.append(change)
        gen_name = gen_name[:2] + gen_name[-3:]
        gen_done_name = ''.join(gen_name)
    gen_mail = []
    for h in mail:
        shift_h = ord(h) + 4
        change_h = chr(shift_h)
        gen_mail.append(change_h)
        gen_mail_2 = gen_mail[:4] + gen_mail[-4:]
        gen_done_mail = ''.join(gen_mail_2)
    e_ticket_clean = gen_done_name +gen_done_mail+ film + starttijd
    print(e_ticket_clean)

codegenerator(name, mail, film, starttijd)
