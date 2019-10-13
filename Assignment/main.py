from network import Person, Post, SocialNetwork

from typing import Tuple


def possible_connections(network: SocialNetwork, person: Person) -> Tuple[int, int]:
    def _possible_connections(target_person: Person, person: Person,
                              likes: int, following: int) -> Tuple[int, int]:
        person._visited = True
        if person is not target_person:
            for p in person.posts:
                if not hasattr(p, "_visited"):
                    likes += 1
                    if not target_person.is_following(p.poster):
                        following += 1
                    p._visited = True
        for p in person.liked_posts:
            if p.poster is not target_person:
                if not hasattr(p, "_visited"):
                    likes += 1
                    if not target_person.is_following(p.poster):
                        following += 1
                    p._visited = True
        for p in person.following:
            if not hasattr(p, "_visited"):
                likes, following = _possible_connections(target_person, p, likes, following)
        return likes, following

    likes, following = _possible_connections(person, person, 0, person.following_count)
    for person in network.people:
        try:
            del person._visited
        except AttributeError:
            pass
    return likes, following


network = SocialNetwork(6, 2)

person1 = network.add_person("person1")
person2 = network.add_person("person2")
person3 = network.add_person("person3")
person4 = network.add_person("person4")
person5 = network.add_person("person5")
person6 = network.add_person("person6")

post1 = person3.make_post("post1")
post2 = person5.make_post("post2")
post3 = person1.make_post("post3")

person1.follow(person2)
person2.follow(person3)
person2.follow(person4)
person4.follow(person1)
person4.follow(person5)
person5.follow(person6)

person2.like_post(post1)
#person6.like_post(post2)

likes, follows = possible_connections(network, person4)

pass
