class VarUtil:
    _global_cache = {}

    @classmethod
    def set_var(cls, k, v):
        cls._global_cache[k] = v

    @classmethod
    def get_var(cls, k):
        return cls._global_cache.get(k, "")

    @classmethod
    def replace(cls, data):
        if isinstance(data, dict): return {k: cls.replace(v) for k, v in data.items()}
        if isinstance(data, list): return [cls.replace(i) for i in data]
        if isinstance(data, str):
            for k, v in cls._global_cache.items():
                data = data.replace(f"${{k}}", str(v))
            return data
        return data



