## AWS KMS Construct Library

Defines a KMS key:

```js
new EncryptionKey(this, 'MyKey', {
    enableKeyRotation: true
});
```

Add a couple of aliases:

```js
const key = new EncryptionKey(this, 'MyKey');
key.addAlias('alias/foo');
key.addAlias('alias/bar');
```

### Sharing keys between stacks

To use a KMS key in a different stack in the same CDK application,
pass the construct to the other stack:

```ts

/**
 * Stack that defines the key
 */
class KeyStack extends cdk.Stack {
  public readonly key: kms.EncryptionKey;

  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    this.key = new kms.EncryptionKey(this, 'MyKey', { retain: false });
  }
}

interface UseStackProps extends cdk.StackProps {
  key: kms.IEncryptionKey; // Use IEncryptionKey here
}

/**
 * Stack that uses the key
 */
class UseStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props: UseStackProps) {
    super(scope, id, props);

    // Use the IEncryptionKey object here.
    props.key.addAlias('alias/foo');
  }
}

const keyStack = new KeyStack(app, 'KeyStack');
new UseStack(app, 'UseStack', { key: keyStack.key });
```


### Importing existing keys

To use a KMS key that is not defined in this CDK app, but is created through other means, use
`EncryptionKey.import(parent, name, ref)`:

```ts
const myKeyImported = EncryptionKey.import(this, 'MyImportedKey', {
    keyArn: 'arn:aws:...'
});

// you can do stuff with this imported key.
key.addAlias('alias/foo');
```

Note that a call to `.addToPolicy(statement)` on `myKeyImported` will not have
an affect on the key's policy because it is not owned by your stack. The call
will be a no-op.

