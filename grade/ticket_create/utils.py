# -*- coding: utf-8 -*-
from Crypto.PublicKey                      import RSA
from Crypto.Random.random                  import getrandbits, \
                                                  randint
from itertools                             import product
from commands                              import *
 
from django.db.models                      import Q
from django.utils.safestring               import SafeUnicode

from fereol.enrollment.subjects.models     import Subject, \
                                                  Group                                              
from fereol.enrollment.records.models      import Record 
from fereol.grade.poll.models              import Poll
from fereol.grade.ticket_create.models     import PublicKey, \
                                                  PrivateKey, \
                                                  UsedTicketStamp 
from fereol.grade.ticket_create.exceptions import *

RAND_BITS = 512 

def gcd( a, b ):
    if b > a:
        a, b = b, a
    while a:
            a, b = b%a, a
    return b
      
def gcwd( u, v ):
	u1 = 1
	u2 = 0
	u3 = u
	v1 = 0
	v2 = 1
	v3 = v
	while v3 != 0:
		q = u3 / v3
		t1 = u1 - q * v1
		t2 = u2 - q * v2
		t3 = u3 - q * v3
		u1 = v1
		u2 = v2
		u3 = v3
		v1 = t1
		v2 = t2
		v3 = t3
	return u1, u2, u3
    
def expMod( a, b, q ):
    p = 1
    
    while b > 0:
        if b & 1:
            p = (p * a) % q
        a = (a * a) % q
        b /= 2
    return p
            
def revMod( a, m ):
    x, y, d = gcwd( a, m )
    
    if d != 1: return -1
    
    x %= m
    if x < 0: x += m
    return x

def poll_cmp( poll1, poll2 ):
    if poll1.group:
        if poll2.group:
            return cmp( poll1.group.subject, poll2.group.subject )
        else:
            return 1
    else:
        if poll2.group:
            return -1
        else:
            return 0
         
def generate_rsa_key():
    """ 
        Generates RSA key - that is, a pair (public key, private key)
        both exported in PEM format 
    """    
    
    #wersja bezpieczniejsza
    key_length = 1024
    RSAkey     = RSA.generate(key_length)    
    
    #wersja szybsza
    #do poprawki: tworzenie i usuwanie pliku test_rsa...
    #getstatusoutput('ssh-keygen -b 1024 -t "rsa" -f test_rsa -N "" -q')
    #RSAkey = RSA.importKey( open('test_rsa').read() )
    #getstatusoutput('rm test_rsa*')
        
    privateKey = RSAkey.exportKey()        
    publicKey  = RSAkey.publickey().exportKey()
    return (publicKey, privateKey)
    
def save_public_keys(polls_public_keys):
    for (poll, key) in polls_public_keys:
        pkey = PublicKey(   poll = poll,
                            public_key = key)
        pkey.save()
    
def save_private_keys(polls_private_keys):
    for (poll, key) in polls_private_keys:
        pkey = PrivateKey(  poll = poll,
                            private_key = key)
        pkey.save()

def generate_keys_for_polls():
    poll_list = Poll.get_current_semester_polls_without_keys()
    pub_list  = []
    priv_list = []
    for el in poll_list:
        (pub, priv) = generate_rsa_key()
        pub_list.append(pub)
        priv_list.append(priv)
    save_public_keys(zip(poll_list, pub_list))
    save_private_keys(zip(poll_list, priv_list))
    return 
    
def group_polls_by_subject( poll_list ):
    if poll_list == []: return []
    
    poll_list.sort( poll_cmp )
    
    res       = []
    act_polls = []
    act_group = poll_list[ 0 ].group
    
    for poll in poll_list:
        if not act_group:
            if not poll.group:
                act_polls.append( poll )
            else:
                act_group = poll.group
                res.append( act_polls )
                act_polls = [ poll ]
        else:
            if poll.group:
                if act_group.subject == poll.group.subject:
                    act_polls.append( poll )
                else:
                    act_group = poll.group
                    res.append( act_polls )
                    act_polls = [ poll ]
            else:
                act_group = poll.group
                res.append( act_polls )
                act_polls = [ poll ]
                
    res.append( act_polls )
    
    return res

def connect_groups( groupped_polls, form ):
    connected_groups = []
    for polls in groupped_polls:
        if not polls[ 0 ].group:
            label = 'join_common'
        else:
            label = u'join_' + unicode( polls[ 0 ].group.subject.pk )
        
        if len( polls ) == 1:
            connected_groups.append( polls )
        elif form.cleaned_data[ label ]:
            connected_groups.append( polls )
        else:
            for poll in polls:
                connected_groups.append([ poll ])
    return connected_groups

def generate_keys( poll_list ):
    keys = []

    for poll in poll_list:
        key =  RSA.importKey( PublicKey.objects.get( poll = poll ).public_key )
        keys.append((unicode(key.n), unicode(key.e)))

    return keys


def check_poll_visiblity( user, poll ):
    if not poll.is_student_entitled_to_poll( user.student ): 
        raise InvalidPollException
    
def check_ticket_not_signed( user, poll ):
    u = UsedTicketStamp.objects.filter( student = user.student, poll = poll )
    if u: 
        raise TicketUsed
        
def mark_poll_used( user, poll ):
    u = UsedTicketStamp( student = user.student,
                         poll    = poll )
    u.save()

def ticket_check_and_mark( user, poll, ticket ):
    check_poll_visiblity( user, poll )
    check_ticket_not_signed( user, poll )
    mark_poll_used( user, poll )
    
def ticket_check_and_sign( user, poll, ticket ):
    check_poll_visiblity( user, poll )
    check_ticket_not_signed( user, poll )
    key    = PrivateKey.objects.get( poll = poll )
    signed = key.sign_ticket( ticket )
    mark_poll_used( user, poll )

def ticket_check_and_sign_without_mark( user, poll, ticket ):
    check_poll_visiblity( user, poll )
    check_ticket_not_signed( user, poll )
    key    = PrivateKey.objects.get( poll = poll )
    signed = key.sign_ticket( ticket )
    return signed

def secure_signer_without_save( user, g, t ):
    try:
        return ticket_check_and_sign_without_mark( user, g, t ), 
    except InvalidPollException:
        return u"Nie masz uprawnień do tej ankiety",
    except TicketUsed:
        return u"Bilet już pobrano",

def secure_mark ( user, g, t ):    
    try:
        return ticket_check_and_mark( user, g, t ), 
    except InvalidPollException:
        return u"Nie masz uprawnień do tej ankiety",
    except TicketUsed:
        return u"Bilet już pobrano",

def secure_signer( user, g, t ):
    try:
        return ticket_check_and_sign( user, g, t ), 
    except InvalidPollException:
        return u"Nie masz uprawnień do tej ankiety",
    except TicketUsed:
        return u"Bilet już pobrano",

def unblind( poll, st ):
    st  = st[0]
    if   st == u"Nie masz uprawnień do tej ankiety":
        return st
    elif st == u"Bilet już pobrano":
        return st
    else:
        st  = st[0]
        key = RSA.importKey( PublicKey.objects.get( poll = poll ).public_key )
        return (unicode(st), unicode(key.n))
        
def get_valid_tickets( tl ):
    err = []
    val = []
    for g, t, st in tl:
        if st == u"Nie masz uprawnień do tej ankiety" or \
           st == u"Bilet już pobrano":
                err.append(( g, st ))
        else:
                val.append(( g, t, st ))
    
    return err, val
        
def to_plaintext( vtl ):
    res = ""
    for p, t, st in vtl:
        res += '[' + p.title + ']'
        if not p.group:
            res += u'Ankieta ogólna &#10;'
        else:
            res += p.group.subject.name + " &#10;"
            res += p.group.get_type_display() + ": "
            res += p.group.get_teacher_full_name() + " &#10;"
        if p.studies_type:
            res += u'dla studiów ' + p.studies_type + " &#10;"
            
        res += unicode( t ) + " &#10;"
        res += unicode( st ) + " &#10;"
        res += "---------------------------------- &#10;"
    return SafeUnicode( unicode( res ))

def from_plaintext( tickets_plaintext ):
    pre_tickets = tickets_plaintext.split('\n')
    tickets_and_signed = []
    tickets = []
    for pre_ticket in pre_tickets:
        try:
            t = int( pre_ticket )
            tickets_and_signed.append( t )
        except:
            pass
    for i in range(0, len( tickets_and_signed )-1, 2):
        ( t, st ) = ( tickets_and_signed[ i ], tickets_and_signed[ i+1 ] )
        tickets.append(( t, st ))
    return tickets