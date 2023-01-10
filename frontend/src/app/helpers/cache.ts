class CacheEntry<T> {

  private _value: T;
  private readonly expiresAt: number;

  constructor(value: T, expiresIn: number) {
    this._value = value;
    this.expiresAt = Date.now() + expiresIn;
  }

  set value(value: T) {
    this._value = value;
  }

  get value(): T {
    return this._value;
  }

  get expired(): boolean {
    return Date.now() > this.expiresAt;
  }
}

type CacheAccessor = string;

class CacheManager {
  private cacheEntries: Map<CacheAccessor, CacheEntry<any>> = new Map();

  public get<T>(className: string, methodName: string, argHash: string): T {
    if (this.has(className, methodName, argHash)) {
      return this.cacheEntries.get(CacheManager.getAccessor(className, methodName, argHash))!.value;
    }
    throw Error('Cache entry not found');
  }

  public has(className: string, methodName: string, argHash: string): boolean {
    const accessor = CacheManager.getAccessor(className, methodName, argHash);
    return this.cacheEntries.has(accessor) && !this.cacheEntries.get(accessor)!.expired;
  }

  public save(className: string, methodName: string, argHash: string, value: any, expiresIn: number): void {
    const accessor = CacheManager.getAccessor(className, methodName, argHash);
    this.cacheEntries.set(accessor, new CacheEntry(value, expiresIn));
  }

  private static getAccessor(className: string, methodName: string, argHash: string): string {
    return `${className}-${methodName}-${argHash}`;
  }

}

const hashArgs = (...args: any) => {
  return btoa(JSON.stringify(args));
};

const cacheManager = new CacheManager();

export const cache = (ttl = 60) => {
  return (target: any, propertyKey: string, descriptor: PropertyDescriptor) => {
    const originalFunction = descriptor.value;

    descriptor.value = function (...args: any) {
      const argHash = hashArgs(args);
      const className = target.constructor.name;
      if (cacheManager.has(className, propertyKey, argHash)) {
        return cacheManager.get(className, propertyKey, argHash);
      }

      const returnValue = originalFunction.apply(this, ...args);
      cacheManager.save(className, propertyKey, argHash, returnValue, ttl * 1000);
      return returnValue;
    };
  };
};
