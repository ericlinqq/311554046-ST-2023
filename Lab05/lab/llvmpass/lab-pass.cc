/*
  Ref:
  * https://llvm.org/doxygen/
  * https://llvm.org/docs/GettingStarted.html
  * https://llvm.org/docs/WritingAnLLVMPass.html
  * https://llvm.org/docs/ProgrammersManual.html
 */
#include "lab-pass.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Constants.h"


using namespace llvm;

char LabPass::ID = 0;

bool LabPass::doInitialization(Module &M) {
  return true;
}

static void dumpIR(Function &F)
{
  for (auto &BB : F) {
    errs() << "BB: " << "\n";
    errs() << BB << "\n";
  }
}

static Constant* getI8StrVal(Module &M, char const *str, Twine const &name) {
  LLVMContext &ctx = M.getContext();

  Constant *strConstant = ConstantDataArray::getString(ctx, str);

  GlobalVariable *gvStr = new GlobalVariable(M, strConstant->getType(), true,
    GlobalValue::InternalLinkage, strConstant, name);

  Constant *zero = Constant::getNullValue(IntegerType::getInt32Ty(ctx));
  Constant *indices[] = { zero, zero };
  Constant *strVal = ConstantExpr::getGetElementPtr(Type::getInt8PtrTy(ctx),
    gvStr, indices, true);

  return strVal;
}

static FunctionCallee printfPrototype(Module &M) {
  LLVMContext &ctx = M.getContext();

  FunctionType *printfType = FunctionType::get(
    Type::getInt32Ty(ctx),
    { Type::getInt8PtrTy(ctx) },
    true);

  FunctionCallee printfCallee = M.getOrInsertFunction("printf", printfType);

  return printfCallee;
}

bool LabPass::runOnModule(Module &M) {
  errs() << "runOnModule\n";

  LLVMContext &ctx = M.getContext();

  FunctionCallee printfCallee = printfPrototype(M);

  // create a global variable 'depth'
  M.getOrInsertGlobal("depth", Type::getInt32Ty(ctx));
  GlobalVariable *globalVariable = M.getNamedGlobal("depth");
  globalVariable->setLinkage(GlobalValue::CommonLinkage);
  globalVariable->setAlignment(MaybeAlign(4));  

  ConstantInt *const_int_val = ConstantInt::get(ctx, APInt(32, 0));
  globalVariable->setInitializer(const_int_val);

  // formatString to print
  Constant *formatString = getI8StrVal(M, "%*s%s: %p\n", "formatString");

  // create indent string
  Constant *indent = getI8StrVal(M, "", "indent");

  for (auto &F : M) {
    if (F.empty()) {
      continue;
    }

    errs() << F.getName() << "\n";

    // TODO  
    // Get Function Name
    Constant *funcName = getI8StrVal(M, F.getName().str().c_str(), "funcName");

    // Get Function Address
    Constant *func_getbitcast = ConstantExpr::getBitCast(&F, Type::getInt8PtrTy(ctx));
    
    // Basic Block
    BasicBlock &Bstart = F.front();
    BasicBlock &Bend = F.back();

    // Split "ret" from original basic block
    Instruction &ret = *(++Bend.rend());
    BasicBlock *Bret = Bend.splitBasicBlock(&ret, "ret");
    
    // Create epilogue BB before ret BB
    BasicBlock *Bepi = BasicBlock::Create(ctx, "epi", &F, Bret);

    // Patch the instruction at end of Bend BB, "br ret", to "br epi"
    Instruction &br = *(++Bend.rend());
    IRBuilder<> BuilderBr(&br);

    BuilderBr.CreateBr(Bepi);

    br.eraseFromParent();

    // Insert code at prologue
    Instruction &Istart = Bstart.front();
    IRBuilder<> BuilderStart(&Istart);
    
    // Load depth
    LoadInst *Load = BuilderStart.CreateLoad(Type::getInt32Ty(ctx), globalVariable);

    // Increment depth and store
    Value *Inc = BuilderStart.CreateAdd(BuilderStart.getInt32(1), Load);
    StoreInst *Store = BuilderStart.CreateStore(Inc, globalVariable); 

    // Print current function information
    std::vector<Value *> args({formatString, Load, indent, funcName, func_getbitcast});
    BuilderStart.CreateCall(printfCallee, args);

    // Insert code at epilogue
    IRBuilder<> BuilderEnd(Bepi);

    // store the original depth (the value that hasn't increment yet)
    StoreInst *Store2 = BuilderEnd.CreateStore(Load, globalVariable);
    BuilderEnd.CreateBr(Bret);

    // Dump IR
    dumpIR(F);
  }

  return true;
}

static RegisterPass<LabPass> X("labpass", "Lab Pass", false, false);