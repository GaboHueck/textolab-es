import random
from collections import defaultdict
from typing import List, Tuple, Dict, Optional

#Given a tuple containing a '.', replace any tokens before '.' into None
def replace_before_point(tup: tuple) -> tuple:
    new_tup = []
    passed_point_flag = False
    for p in list(tup):
        if p == '.':
            passed_point_flag = True
            new_tup.append(p)
        else:
            if passed_point_flag:
                new_tup.append(p)
            else:
                new_tup.append(None)       #Anything before the point is turned into None 
    out_tup = tuple(new_tup)
    return out_tup

class MarkovBabbler:
    """
    Simple n-gram Markov text trainer and generator.

    Parameters
    ----------
    n : int
        Order of the n-gram used to build the Markov chain. For example, n=2
        corresponds to a bigram-based model, n=3 to a trigram-based model.
    point_blind : bool
        Default = True
        Tells the model to have no token preference if a '.' character occurs, which
        means that all sentences may end and start without probabilistic bias.

    Methods
    -------
    train(tokens)
        Trains the Markov model on a sequence of tokens.

        Parameters
        ----------
        tokens : list[str]
            A list of pre-tokenized text tokens used to estimate transition
            probabilities for the Markov chain.

        Returns
        -------
        None

    generate(N)
        Generates a text sequence using the trained Markov model.

        Parameters
        ----------
        N : int
            Number of tokens to generate.

        Returns
        -------
        str
            A generated string consisting of N tokens sampled from the
            Markov chain.
    """
    def __init__(self, order: int = 2, point_blind: bool = True):
        self.n = order
        self.model: Dict[Tuple[str, ...], List[str]] = defaultdict(list)
        self.point_blind = point_blind
    
    def train(self, tokens: List[str]) -> None:
        #Trains the model resulting in a dict of [Tuple(n), List]
        if len(tokens) < self.n + 1:
            raise ValueError(f"Token list must contain at least {self.n + 1} tokens.")
        
        for i in range(len(tokens) - self.n):
            prefix = tuple(tokens[i:i + self.n])            # n-gram (key)
            if self.point_blind and '.' in prefix:          # If model is blinded, checks if possible tuple contains a point
                prefix = replace_before_point(prefix)       # Replace all tokens before '.' with None
            next_token = tokens[i + self.n]                 # the token that follows (value)
            self.model[prefix].append(next_token)

     
    def generate(self, max_tokens: int = 50, seed: Optional[Tuple[str, ...]] = None) -> str:
        if not self.model:
            raise ValueError("Model is empty. Did you forget to call train()?")

        if seed:
            if len(seed) != self.n:
                raise ValueError(f"Seed must be a list of {self.n} tokens.")
            current_prefix = tuple(seed)
            if current_prefix not in self.model:
                raise ValueError("Seed not found in model.")
        else:
            current_prefix = random.choice(list(self.model.keys()))
            print(f'No seed given. "{current_prefix}" n-gram chosen to start with.\n')

        generated = list(current_prefix)

        for _ in range(max_tokens - self.n):
            #Transforms anything before the point into None (if model is blinded)
            if self.point_blind and '.' in current_prefix:
                current_prefix = replace_before_point(current_prefix)

            next_tokens = self.model.get(current_prefix)
        
            if not next_tokens:
                print("Warning: Generation stopped before reaching max tokens.")
                break

            next_token = random.choice(next_tokens)
            generated.append(next_token)
            current_prefix = tuple(generated[-self.n:])

        generated_str = ''
        for w in generated:
            if w in [',','.','?','!',':',';',')','...']:
                generated_str += w
            else:
                if len(generated_str) > 0 and generated_str[-1] in ['¿','¡','(']:
                    generated_str = generated_str + w
                else:
                    generated_str = generated_str + ' ' + w

        return generated_str
